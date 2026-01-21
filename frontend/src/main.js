import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'
import { useAuthStore } from './stores/authStore'
import { setUnauthorizedHandler } from './services/api'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Configurar interceptor de errores de autenticación
const authStore = useAuthStore()
setUnauthorizedHandler(() => {
    authStore.logout()
})

app.mount('#app')
