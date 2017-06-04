<template>
  <div id="app">
    <router-view
      :user="user"
      :setProblems="setProblems"
      :setAnwsers="setAnwsers"
      :tasks="tasks"
      :updateWeek="updateWeek"
      :updateDay="updateDay"
      :start="start"
      :problems="problems"></router-view>
  </div>
</template>

<script>
import API from '@/scripts/api'

export default {
  name: 'app',
  data() {
    return {
      user: { name: 1 },
      problems: [],
      tasks: [],
    }
  },
  created() {
    this.fetchUserInfo()
  },
  methods: {
    fetchUserInfo() {
      this.$get(API.getUserInfo).then((res) => {
        this.user = res
      })
    },
    setProblems(data) {
      this.problems = data
    },
    setAnwsers(data) {
      this.tasks = data
    },
    updateWeek(data, num) {
      this.tasks = this.tasks.map((item) => {
        const newitem = item
        if (newitem.id === data.id) newitem.bottom_times = num
        return newitem
      })
    },
    updateDay(data, beginTime, endTime) {
      this.tasks = this.tasks.map((item) => {
        const newitem = item
        if (newitem.id === data.id) {
          newitem.begin_time = beginTime
          newitem.end_time = endTime
        }
        return newitem
      })
    },
    start(decade, hasWeekend, level) {
      const tasks = this.tasks.filter(item => item.choice === level)
                              .map((item) => {
                                const newitem = item
                                return newitem
                              })
      this.$post(API.startPlan, {
        has_weekend: hasWeekend ? 1 : 0,
        week_size: decade,
        answers: tasks,
      }).then(() => {
      })
    },
  },
};
</script>

<style>
html, body {
  height: 100%;
}
body hr {
  height: 1px !important;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-height: 100%;
  padding-bottom: .2rem;
  background: #84dff5 url(assets/bg.png) 0 0 / auto .86rem repeat;
}
</style>
