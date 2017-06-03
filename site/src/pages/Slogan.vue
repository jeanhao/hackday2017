<template lang="pug">
#index-wrapper
  .question-wrapper
    div.girl
    div.question
      p 经过测试
      p 我有种强烈的预感
      p 在不久的将来
      p 你会成为一个
      h3.great-people 伟大的人
      p 为了助你达成这一计划
      p 我们特此为你定制了一份
      div.plan(@click="startPlan") 咸鱼翻身计划
</template>

<script>
export default {
  name: 'Slogan',
  data() {
    return {
    }
  },
  methods: {
    startPlan() {
      this.$router.push({ path: 'list' })
    },
  },
}
</script>

<style lang='scss' scoped>
#index-wrapper {
  font-size: .16rem;
  text-align: left;
  height: 100%;
}
.question-wrapper {
  background-color: rgba(0,0,0,.5);
  color: #ffffff;
  position: relative;
  height: 100%;
  &:after {
    content: '';
    display: block;
    clear: both;
  }
  .girl {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translateY(-70%);
    width: 50%;
    height: 2.15rem;
    background: url(../assets/girl.png) .15rem center / 80% auto no-repeat;
  }
  .question {
    margin-top: 1.2rem;
    font-size: 14px;
    width: 50%;
    float: right;
    padding-right: .3rem;
    box-sizing: border-box;
    h3.great-people {
      color: #fdf147 !important;
      font-size: .34rem;
      line-height: .6rem !important;
    }
    .gutter {
      height: .15rem;
      width: 100%;
    }
  }
}
.plan {
  margin-top: .4rem;
  display: inline-block;
  padding: 0 .25rem;
  box-sizing: border-box;
  line-height: .36rem;
  color: #ffffff;
  border: 2px solid #ffffff;
  border-radius: .18rem;
}
</style>
