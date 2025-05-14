
import piniaPluginPersist from 'pinia-plugin-persist' //++++
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import '@/styles/common.css'
const app = createApp(App)

app.use(createPinia().use(piniaPluginPersist))
app.use(router)

app.mount('#app')
