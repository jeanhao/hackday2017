// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';

import Mobile from '@/scripts/until'

import vFetch from '@/plugins/vFetch'
import Tip from '@/plugins/Tip/Tip'

import '@/libs/typo.css'

import App from './detail';

const mb = new Mobile()
mb.setFontSize()

Vue.config.productionTip = false;

Vue.use(Tip)
Vue.use(vFetch)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
});
