<template lang="pug">
#index-wrapper
  h2 亲爱的{{user.name}}，请回答以下问题
  ul.problems-wrapper
    li(v-for="item in problems",
      key="item.id",
      @click="handleProblemClick(item)"
      :class="{active: chooseProblems.includes(item.id)}") {{item.content}}
  mu-raised-button(primary, @click="setProblems") 提交
</template>

<script>
import API from '@/scripts/api'

export default {
  name: 'SetQuestion',
  data() {
    return {
      chooseProblems: [],
    }
  },
  props: {
    user: Object,
    problems: Array,
    setAnwsers: Function,
  },
  created() {
  },
  methods: {
    handleProblemClick(problem) {
      const { chooseProblems } = this
      if (chooseProblems.includes(problem.id)) {
        this.chooseProblems = chooseProblems.filter(item => chooseProblems.id !== item)
      } else {
        chooseProblems.push(problem.id)
        this.chooseProblems = chooseProblems
      }
    },
    setProblems() {
      const { chooseProblems } = this
      if (!chooseProblems || chooseProblems.length === 0) {
        this.$tip('请选择你的问题喔！')
        return
      }
      const problems = chooseProblems.join()
      this.$get(API.getAnswers, { problems }).then((data) => {
        this.setAnwsers(data)
        this.$router.push({ path: 'list' })
      })
    },
  },
}
</script>

<style lang='scss' scoped>
#index-wrapper {
  font-size: .16rem;
}
.problems-wrapper {
  .active {
    color: red;
  }
}
</style>
