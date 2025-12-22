<template>
  <div>
    <h1>Iniciar Sesión</h1>
    
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="email">Email/Username:</label>
        <input 
          id="email"
          type="text" 
          v-model="email" 
          required 
          :disabled="authStore.loading"
        />
      </div>
      
      <div>
        <label for="password">Contraseña:</label>
        <input 
          id="password"
          type="password" 
          v-model="password" 
          required 
          :disabled="authStore.loading"
        />
      </div>
      
      <div v-if="authStore.error">
        <p style="color: red;">{{ authStore.error }}</p>
      </div>
      
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')

    const handleSubmit = async () => {
      try {
        await authStore.login({
          email: email.value,
          password: password.value
        })
        // Redirigir a /mascotas si el login es exitoso
        router.push('/mascotas')
      } catch (err) {
        // El error ya está manejado en el store
        // Solo necesitamos capturar para evitar errores no manejados
      }
    }

    return {
      email,
      password,
      authStore,
      handleSubmit
    }
  }
}
</script>

<style scoped>
/* Estilos específicos de la vista */
form {
  max-width: 400px;
  margin: 0 auto;
}

div {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>

