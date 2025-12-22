// Servicio para endpoints de mascotas
import { apiRequest } from './api.js'

/**
 * Obtiene la lista de mascotas desde la API
 * @returns {Promise<Array>} - Array de mascotas
 */
export async function getMascotas() {
  const mascotas = await apiRequest('/mascotas/', {
    method: 'GET'
  })
  return mascotas
}

/**
 * Obtiene el detalle de una mascota por UUID
 * @param {string} uuid - UUID de la mascota
 * @returns {Promise<Object>} - Objeto con los datos de la mascota
 */
export async function getMascotaByUUID(uuid) {
  const mascota = await apiRequest(`/mascotas/${uuid}/`, {
    method: 'GET'
  })
  return mascota
}

/**
 * Toggle de like en una mascota
 * @param {string} uuid - UUID de la mascota
 * @returns {Promise<Object>} - Objeto con {Liked: boolean, msj?: string}
 */
export async function toggleLikeMascota(uuid) {
  const response = await apiRequest(`/mascotas/${uuid}/toggle-like/`, {
    method: 'POST'
  })
  return response
}
