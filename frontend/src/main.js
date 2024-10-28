import { createApp } from 'vue'
import { createBootstrap } from 'bootstrap-vue-next'
import router from "./router"
import store from "./store"
import axios from 'axios'
import App from './App.vue'

import { LoadingPlugin } from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/css/index.css'

// Add the necessary CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://localhost:8000"


const app = createApp(App)
app.use(createBootstrap())
app.use(LoadingPlugin)
app.use(store)
app.use(router)
app.mount('#app')
