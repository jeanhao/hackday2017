import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/pages/Login'
// import HomePage from '@/pages/HomePage'
import SaveMe from '@/pages/SaveMe'
import SetQuestion from '@/pages/SetQuestion'
import TaskList from '@/pages/TaskList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'SaveMe',
      component: SaveMe,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/question',
      name: 'SetQuestion',
      component: SetQuestion,
    },
    {
      path: '/list',
      name: 'TaskList',
      component: TaskList,
    },
  ],
});
