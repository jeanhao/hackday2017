<template>
  <div id="app">
    <router-view
      :user="user"
      :setProblems="setProblems"
      :setAnwsers="setAnwsers"
      :tasks="tasks"
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
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
