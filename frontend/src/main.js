import 'bootstrap/dist/css/bootstrap.css'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

Vue.use(BootstrapVue)
Vue.use(Vuelidate)
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000";

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
