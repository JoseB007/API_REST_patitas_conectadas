<template>
  <div>
    <h1>Mascotas</h1>
    
    <div v-if="mascotasStore.loading">
      Cargando...
    </div>
    
    <div v-else-if="mascotasStore.error">
      Error: {{ mascotasStore.error }}
    </div>
    
    <div v-else>
      <ul>
        <li v-for="mascota in mascotasStore.mascotas" :key="mascota.url">
          <MascotaCard :mascota="mascota" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useMascotasStore } from '../stores/mascotasStore.js'
import MascotaCard from '../components/mascotas/MascotaCard.vue'

export default {
  name: 'MascotasView',
  components: {
    MascotaCard
  },
  setup() {
    const mascotasStore = useMascotasStore()

    onMounted(async () => {
      await mascotasStore.fetchMascotas()
    })

    return {
      mascotasStore
    }
  }
}
</script>

<style scoped>
/* Estilos específicos de la vista */
</style>
