<template lang="pug">
#index-wrapper
  .question-wrapper
    div.girl
    div.question
      p 亲爱的{{user.name}}
      p 我是你的咸鱼鼓励师白云
      p 为了深入的了解你
      div.gutter
      p 希望你在下面的属性中
      p 点亮最适合自己的3-5个
  ul.tags-wrapper
    li(v-for="item in tags",
      key="item.id",
      @click="handleTagClick(item)"
      :class="{active: chooseTags.includes(item.id)}") {{item.tag_name}}
  div.submit-button(@click="setTags")
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
  padding-top: .37rem;
  text-align: left;
}
.question-wrapper {
  background-color: rgba(0,0,0,.5);
  color: #ffffff;
  padding: .2rem 0;
  position: relative;
  min-height: 1.5rem;
  &:after {
    content: '';
    display: block;
    clear: both;
  }
  .girl {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-50%);
    width: 50%;
    height: 2.15rem;
    background: url(../assets/girl.png) .15rem center / 80% auto no-repeat;
  }
  .question {
    font-size: 13px;
    width: 50%;
    float: right;
    padding-right: .3rem;
    box-sizing: border-box;
    .gutter {
      height: .15rem;
      width: 100%;
    }
  }
}
.tags-wrapper {
  margin-top: .7rem;
  padding: 0 .22rem;
  &:after {
    content: '';
    display: block;
    clear: both;
  }
  li {
    margin-bottom: .08rem;
    margin: 0 .06rem .08rem;
    font-size: 14px;
    float: left;
    padding: .12rem .2rem;
    color: #2b75c1;
    line-height: 1;
    background-color: #ffffff;
    border-radius: .2rem;
    border: 1px solid #2b75c1;
    transition: color .3s ease, background-color .3s ease;
  }
  .active {
    background-color: #2b75c1;
    color: #ffffff;
  }
}
.submit-button {
  position: fixed;
  bottom: .35rem;
  left: 50%;
  transform: translateX(-50%);
  width: .63rem;
  height: .63rem;
  background: #2b76c2 url(../assets/arrow.png) center center / auto .25rem no-repeat;
  border-radius: 50%;
  box-shadow: 0 3px 10px rgba(0,0,0,.156863), 0 3px 10px rgba(0,0,0,.227451);
}
</style>
