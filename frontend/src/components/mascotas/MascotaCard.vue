<template>
  <div>
    <h3>
      <router-link :to="`/mascotas/${getMascotaUUID()}`">
        {{ mascota.nombre }}
      </router-link>
    </h3>
    <p>{{ mascota.descripcion || 'Sin descripción' }}</p>
    <button @click="handleLike">Like ({{ likesCount }})</button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useMascotasStore } from '../../stores/mascotasStore.js'

export default {
  name: 'MascotaCard',
  props: {
    mascota: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const mascotasStore = useMascotasStore()
    const localLikes = ref(null)

    const getMascotaUUID = () => {
      // Si el objeto tiene uuid, usarlo directamente
      if (props.mascota.uuid) {
        return props.mascota.uuid
      }
      // Si no, extraerlo de la URL que viene en el formato: http://localhost:8000/mascotas/{uuid}/
      if (props.mascota.url) {
        const parts = props.mascota.url.split('/')
        // El UUID está en la penúltima parte antes del slash final
        return parts[parts.length - 2] || parts[parts.length - 1]
      }
      return null
    }

    // Inicializar el contador local con el valor de la prop
    onMounted(() => {
      localLikes.value = props.mascota.likes || 0
    })

    // Usar contador local si existe, sino usar el de la prop
    const likesCount = computed(() => {
      return localLikes.value !== null ? localLikes.value : (props.mascota.likes || 0)
    })

    const handleLike = async () => {
      const uuid = getMascotaUUID()
      if (!uuid) return

      // Actualización optimista: incrementar el contador inmediatamente
      if (localLikes.value !== null) {
        localLikes.value += 1
      } else {
        localLikes.value = (props.mascota.likes || 0) + 1
      }

      // Llamar al store (aunque aún es un stub)
      await mascotasStore.likeMascota(uuid)
    }

    return {
      likesCount,
      handleLike,
      getMascotaUUID
    }
  }
}
</script>

<style scoped>
/* Estilos específicos del componente */
</style>
