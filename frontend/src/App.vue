<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/authStore'

const authStore = useAuthStore()

onMounted(async () => {
  try {
    await authStore.fetchUser()
  } catch (error) {
    // Si falla (por ejemplo, token expirado o inexistente), no hacemos nada,
    // el usuario simplemente no estará autenticado.
  }
})
</script>

<style>
/* Estilos globales */
</style>
