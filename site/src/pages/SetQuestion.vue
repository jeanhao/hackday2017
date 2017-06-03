<template lang="pug">
#index-wrapper
  .question-wrapper
    div.girl
    div.question
      p 下列哪些事件是您生活的常态？
  ul.problems-wrapper
    li(v-for="item in problems",
      key="item.id",
      @click="handleProblemClick(item)"
      :class="{active: chooseProblems.includes(item.id)}") {{item.content}}
  div.submit-wrapper
    div.submit-button(@click="setProblems") 点击即可翻身
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
        this.chooseProblems = chooseProblems.filter(item => problem.id !== item)
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
        this.$router.push({ path: 'slogan' })
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
  min-height: 1.5rem;
  position: relative;
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

.problems-wrapper {
  margin-top: .45rem;
  padding: .25rem;
  &:after {
    content: '';
    display: block;
    clear: both;
  }
  li {
    width: 100%;
    margin-bottom: .05rem;
    font-size: 14px;
    float: left;
    padding: .12rem .2rem;
    box-sizing: border-box;
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

.submit-wrapper {
  text-align: center;
}

.submit-button {
  display: inline-block;
  padding: 0 .25rem;
  box-sizing: border-box;
  line-height: .36rem;
  color: #ffffff;
  background: #2b76c2;
  border-radius: .18rem;
  box-shadow: 0 3px 10px rgba(0,0,0,.156863), 0 3px 10px rgba(0,0,0,.227451);
}
</style>
