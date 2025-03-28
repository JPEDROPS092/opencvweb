import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

// Configuração global do Axios
axios.defaults.baseURL = 'http://localhost:8000/api/'

const app = createApp(App)

// Disponibiliza o axios globalmente na aplicação
app.config.globalProperties.$axios = axios

app.use(store)
   .use(router)
   .use(vuetify)
   .mount('#app')
