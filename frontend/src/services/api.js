// Cliente HTTP base usando fetch nativo
const API_BASE_URL = 'http://localhost:8000'

/**
 * Función base para realizar peticiones HTTP a la API
 * @param {string} endpoint - Endpoint relativo (ej: '/mascotas/')
 * @param {object} options - Opciones de fetch (method, body, headers, etc.)
 * @returns {Promise<*>} - Respuesta JSON parseada
 * @throws {Error} - Si la respuesta HTTP tiene status >= 400
 */
export async function apiRequest(endpoint, options = {}) {
  // Construir URL completa
  const url = `${API_BASE_URL}${endpoint}`

  // Headers por defecto
  const defaultHeaders = {
    'Content-Type': 'application/json'
  }

  // Combinar headers por defecto con los proporcionados
  const headers = {
    ...defaultHeaders,
    ...options.headers
  }

  // Configuración de fetch
  const fetchOptions = {
    ...options,
    headers,
    credentials: 'include' // Incluir cookies para autenticación JWT
  }

  try {
    const response = await fetch(url, fetchOptions)

    // Manejar errores HTTP (status >= 400)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      const error = new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`)
      error.status = response.status
      error.data = errorData
      throw error
    }

    // Retornar JSON parseado
    return await response.json()
  } catch (error) {
    // Si ya es un error HTTP que lanzamos, re-lanzarlo
    if (error.status) {
      throw error
    }
    // Si es error de red u otro error, envolverlo
    throw new Error(`Network error: ${error.message}`)
  }
}
