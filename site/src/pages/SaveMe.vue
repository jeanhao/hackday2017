<template lang="pug">
#index-wrapper
  h2 亲爱的{{user.name}}，以下哪些属性与你最契合？
  ul.tags-wrapper
    li(v-for="item in tags",
      key="item.id",
      @click="handleTagClick(item)"
      :class="{active: chooseTags.includes(item.id)}") {{item.tag_name}}
  mu-raised-button(primary, @click="setTags") 提交
</template>

<script>
import API from '@/scripts/api'

export default {
  name: 'SaveMe',
  data() {
    return {
      tags: [],
      chooseTags: [],
    }
  },
  props: {
    user: Object,
    setProblems: Function,
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.$get(API.getTags).then((res) => {
        this.tags = res
      })
    },
    handleTagClick(tag) {
      const { chooseTags } = this
      if (chooseTags.includes(tag.id)) {
        this.chooseTags = chooseTags.filter(item => tag.id !== item)
      } else {
        chooseTags.push(tag.id)
        this.chooseTags = chooseTags
      }
    },
    setTags() {
      const { chooseTags } = this
      if (!chooseTags || chooseTags.length === 0) {
        this.$tip('请选择你的属性标签喔')
        return
      }
      const tags = chooseTags.join()
      this.$get(API.getProblems, { tags }).then((res) => {
        console.log(1)
        this.setProblems(res)
        this.$router.push({ path: 'question' })
      })
    },
  },
}
</script>

<style lang='scss' scoped>
#index-wrapper {
  font-size: .16rem;
}
.tags-wrapper {
  .active {
    color: red;
  }
}
</style>
