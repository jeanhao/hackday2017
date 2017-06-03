// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';


import MuseUI from 'muse-ui'

import Mobile from '@/scripts/until'

import vFetch from '@/plugins/vFetch'
import Tip from '@/plugins/Tip/Tip'

import 'muse-ui/dist/muse-ui.css'
import '@/libs/typo.css'

import App from './App';
import router from './router';


const mb = new Mobile()
mb.setFontSize()

Vue.config.productionTip = false;

Vue.use(MuseUI)
Vue.use(Tip)
Vue.use(vFetch)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
