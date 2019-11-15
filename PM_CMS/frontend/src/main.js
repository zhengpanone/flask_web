// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Cookies from 'js-cookie'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import App from './App'
import axios from './http'
import router from './router'

Vue.config.productionTip = false

Vue.prototype.$axios = axios

/* eslint-disable no-new */

Vue.use(Element, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
}).$mount('#app')
