// Servicio para endpoints de autenticación
import { apiRequest } from './api.js'

/**
 * Inicia sesión con credenciales
 * @param {Object} credentials - Objeto con email y password
 * @param {string} credentials.email - Email del usuario
 * @param {string} credentials.password - Contraseña del usuario
 * @returns {Promise<Object>} - Datos del usuario autenticado
 */
export async function login(credentials) {
  const response = await apiRequest('/auth/login/', {
    method: 'POST',
    body: JSON.stringify(credentials)
  })
  return response
}

/**
 * Cierra la sesión del usuario actual
 * @returns {Promise<void>}
 */
export async function logout() {
  await apiRequest('/auth/logout/', {
    method: 'POST'
  })
}

/**
 * Obtiene el usuario actual autenticado
 * @returns {Promise<Object>} - Datos del usuario actual
 */
export async function getCurrentUser() {
  const user = await apiRequest('/auth/user/', {
    method: 'GET'
  })
  return user
}

