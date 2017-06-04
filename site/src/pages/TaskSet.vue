<template lang="pug">
#index-wrapper
  mu-dialog(:open="dialog", title="请输入一周执行次数", @close="closeWeek")
    input(type='number', v-model='weekNum', id="week-num")
    mu-flat-button(slot="actions", @click="closeWeek", primary, label="取消")
    mu-flat-button(slot="actions", primary, @click="updateWeekNum", label="确定")
  mu-dialog(:open="dayDialog", title="请确定开始时间和结束时间", @close="closeDay")
    mu-time-picker(hintText="开始时间", format="24hr", v-model='beginTime')
    mu-time-picker(hintText="结束时间", format="24hr", v-model='endTime')
    mu-flat-button(slot="actions", @click="closeDay", primary, label="取消")
    mu-flat-button(slot="actions", primary, @click="updateDayNum", label="确定")
  mu-dialog(:open="decadeDialog", title="请输入执行周期", @close="closeDecade")
    input(type='number', v-model='decade', id="week-num")
    mu-flat-button(slot="actions", @click="closeDecade", primary, label="取消")
    mu-flat-button(slot="actions", primary, @click="sureDecade", label="确定")
  .title 
    span 伟大的人养成计划
    i.share
    //- i.edit
  .task-level
    span 难度：
    i.star(v-for="i in (level + 1)", @click="level === 2 ? (level = 0) : (level++)")
  .task-card
    .task-intro
      .header
        span 疗程周期
        span 疗程一
      .body
        span(@click="decadeDialog=true") {{decade}}
        span(@click="has_weekend=!has_weekend") 一周{{has_weekend ? '七' : '五'}}天
  .task-card
    .daily-task.task-list
      .header 每日计划
      .body
        ul
          li(v-for="item in curDayTasks", @click="showDayDialog(item)")
            span.name {{item.content}}
            span.time {{item.begin_time}} - {{item.end_time}}
  .task-card
    .week-task.task-list
      .header 周计划
      .body
        ul
          li(v-for="item in curWeekTasks", @click="showWeekDialog(item)")
            span.name {{item.content}}
            span.time 一周{{item.bottom_times}}次
  .submit-wrapper
    .submit-button(@click="startMyPlan") 开始我的养成
</template>

<script>
export default {
  name: 'SetQuestion',
  data() {
    return {
      level: 1,
      dialog: null,
      dayDialog: null,
      curClickDay: null,
      curClickWeek: null,
      decadeDialog: null,
      decade: 3,
      weekNum: null,
      beginTime: null,
      endTime: null,
      has_weekend: true,
    }
  },
  props: {
    updateDay: Function,
    updateWeek: Function,
    start: Function,
    tasks: Array,
  },
  computed: {
    curDayTasks() {
      if (!this.tasks) return []
      return this.tasks.filter(item => item.choice === this.level && item.ans_type === 0)
    },
    curWeekTasks() {
      if (!this.tasks) return []
      return this.tasks.filter(item => item.choice === this.level && item.ans_type === 1)
    },
  },
  methods: {
    closeWeek() {
      this.dialog = false
    },
    showWeekDialog(task) {
      this.dialog = true
      this.curClickWeek = task
    },
    showDayDialog(task) {
      this.dayDialog = true
      this.curClickDay = task
    },
    closeDay() {
      this.dayDialog = false
    },
    updateWeekNum() {
      if (!this.weekNum) return
      this.updateWeek(this.curClickWeek, this.weekNum)
      this.dialog = false
      this.weekNum = null
    },
    updateDayNum() {
      if (!this.beginTime || !this.endTime) return
      this.updateDay(this.curClickDay, this.beginTime, this.endTime)
      this.dayDialog = false
    },
    startMyPlan() {
      this.start(this.decade, this.has_weekend, this.level)
    },
    closeDecade() {
      this.decadeDialog = false
      this.decade = 3
    },
    sureDecade() {
      this.decadeDialog = false
    },
  },
}
</script>

<style lang='scss' scoped>
#week-num {
  border: none;
  border-bottom: 1px solid #2b75c1;
  outline: none;
  width: 100%;
}
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
    right: .08rem;
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
.task-list {
  margin-top: .15rem;
  .header {
    font-size: .18rem;
    font-weight: 700;
    text-align: left;
    text-indent: .1rem;
  }
  font-size: 13px;
  li {
    padding: .1rem 0;
    display: flex;
    .name {
      flex: 1;
      text-align: left;
      padding: 0 .1rem;
    }
    .time {
      flex: none;
    }
  }
}
.daily-task {
  li {
    .time {
      display: inline-block;
      width: 1.5rem;
    }
  }
}
.week-task {
  li {
    .time {
      display: inline-block;
      width: .8rem;
    }
  }
}

.submit-wrapper {
  margin-top: .25rem;
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
