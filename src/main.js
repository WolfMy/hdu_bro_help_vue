import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import './plugins/iview.js'
import router from './router'
import store from './store'

/*
import { PasswordInput, NumberKeyboard } from 'vant';
import { Button } from 'vant';

Vue.use(Button);
Vue.use(PasswordInput).use(NumberKeyboard);
*/

Vue.config.productionTip = false
Vue.prototype.$api_baseUrl = 'http://120.27.192.52:8080/';
//Vue.prototype.$api_baseUrl = 'http://127.0.0.1:5000/';
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
