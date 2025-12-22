<template>
  <div>
    <div v-if="loading">
      Cargando...
    </div>
    
    <div v-else-if="error">
      Error: {{ error }}
    </div>
    
    <div v-else-if="mascota">
      <h1>{{ mascota.nombre }}</h1>
      <p>{{ mascota.descripcion || 'Sin descripción' }}</p>
      <img v-if="mascota.foto_url" :src="mascota.foto_url" :alt="mascota.nombre" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMascotaByUUID } from '../services/mascotasService.js'

export default {
  name: 'MascotaDetailView',
  setup() {
    const route = useRoute()
    const mascota = ref(null)
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      try {
        loading.value = true
        error.value = null
        const uuid = route.params.uuid
        const data = await getMascotaByUUID(uuid)
        mascota.value = data
      } catch (err) {
        error.value = err.message || 'Error al cargar la mascota'
      } finally {
        loading.value = false
      }
    })

    return {
      mascota,
      loading,
      error
    }
  }
}
</script>

<style scoped>
/* Estilos específicos de la vista */
</style>

