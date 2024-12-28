import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import $ from 'jquery'

window.$ = window.jQuery = $

const app = createApp(App)

// 设置全局属性
app.config.globalProperties.$ = $

app.use(router)
app.mount('#app')
