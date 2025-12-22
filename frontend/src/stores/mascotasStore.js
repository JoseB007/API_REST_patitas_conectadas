import { defineStore } from 'pinia'
import { getMascotas, toggleLikeMascota } from '../services/mascotasService.js'

export const useMascotasStore = defineStore('mascotas', {
  state: () => ({
    mascotas: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchMascotas() {
      this.loading = true
      this.error = null
      
      try {
        const data = await getMascotas()
        this.mascotas = data
      } catch (err) {
        this.error = err.message || 'Error al cargar las mascotas'
        throw err
      } finally {
        this.loading = false
      }
    },

    async likeMascota(uuid) {
      try {
        const response = await toggleLikeMascota(uuid)
        
        // Actualizar el contador de likes en el estado local
        const mascota = this.mascotas.find(m => {
          // Buscar por UUID extraído de la URL o UUID directo
          const mascotaUuid = m.uuid || (m.url ? m.url.split('/').slice(-2, -1)[0] : null)
          return mascotaUuid === uuid
        })
        
        if (mascota) {
          if (response.Liked) {
            // Incrementar likes si se dio like
            mascota.likes = (mascota.likes || 0) + 1
          } else {
            // Decrementar likes si se quitó el like
            mascota.likes = Math.max(0, (mascota.likes || 0) - 1)
          }
        }
        
        return response
      } catch (err) {
        this.error = err.message || 'Error al dar like a la mascota'
        throw err
      }
    }
  }
})
