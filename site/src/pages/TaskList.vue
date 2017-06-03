<template lang="pug">
#index-wrapper
  .title 
    span 伟大的人养成计划
    i.share
    i.edit
  .task-level
    span 难度：
    i.star(v-for="i in level")
  .task-card
    .task-intro
      .header
        span 疗程周期
        span 疗程一
      .body
        span 3
        span 一周七天
  .task-card
    .daily-task
      .header 每日计划
      .body
        ul
</template>

<script>
export default {
  name: 'SetQuestion',
  data() {
    return {
      level: 2,
    }
  },
  props: {
    tasks: Array,
  },
  created() {
    console.log(this.tasks)
  },
  methods: {
  },
}
</script>

<style lang='scss' scoped>
#index-wrapper {
  font-size: .16rem;
  padding: .15rem .17rem 0;
}
.title {
  font-family: "Source Sans Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: .2rem;
  color: #000000;
  font-weight: 700;
  position: relative;
  i {
    display: inline-block;
    width: .24rem;
    height: .24rem;
    vertical-align: middle;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }
  .edit {
    right: .08rem;
    background: url(../assets/edit.png) center center / 100% 100% no-repeat;
  }
  .share {
    right: .4rem;
    background: url(../assets/share.png) center center / 100% 100% no-repeat;
  }
}
.task-level {
  font-size: 14px;
  color: #2b76c2;
  font-weight: 700;
  .star {
    display: inline-block;
    width: .15rem;
    height: .15rem;
    background: url(../assets/star.png) center center/ 100% 100% no-repeat;
    vertical-align: middle;
    margin-right: .05rem;
  }
}

.task-card {
  background-color: #fff;
  border-radius: 3px;
  box-shadow: 0 3px 10px rgba(130,130,130,.156863), 0 3px 10px rgba(130,130,130,.227451);
}

.task-intro {
  margin-top: .1rem;
  text-align: center;
  padding: .1rem 0;
  .header {
    display: flex;
    color: #000;
    font-size: .18rem;
    font-weight: 500;
    padding: .05rem 0;
    span {
      flex: 1;
    }
  }
  .body {
    display: flex;
    span {
      flex: 1;
    }
  }
}
</style>
