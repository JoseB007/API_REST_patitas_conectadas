// Cliente HTTP base usando fetch nativo
const API_BASE_URL = 'http://localhost:8000'

// Callback para manejar errores de autenticación (logout automático)
let unauthorizedHandler = null

export const setUnauthorizedHandler = (handler) => {
  unauthorizedHandler = handler
}

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

  // Extraer _retry para uso interno y no pasarlo al fetch nativo, construir fetchArgs con los demás parámetros
  const { _retry, ...fetchArgs } = options

  // Configuración de fetch
  const fetchOptions = {
    ...fetchArgs,
    headers,
    credentials: 'include' // Incluir cookies para autenticación JWT
  }

  try {
    const response = await fetch(url, fetchOptions)

    // Lógica de reintento con Refresh Token si recibimos 401
    if (response.status === 401 && !_retry) {
      try {
        // Intentar refrescar el token
        const refreshResponse = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
          method: 'POST',
          credentials: 'include'
        })

        if (refreshResponse.ok) {
          // Si el refresh fue exitoso, reintentar la petición original
          console.log('Token refresh exitoso')
          return apiRequest(endpoint, { ...options, _retry: true })
        } else {
          // Si el refresh falló (por ejemplo, refresh token expirado)
          console.log('Token refresh fallido o expirado')
          if (unauthorizedHandler) unauthorizedHandler()
        }
      } catch (err) {
        // Si falla el refresh (error de red u otros), continuamos para lanzar el error original
        console.error('Error during token refresh:', err)
        if (unauthorizedHandler) unauthorizedHandler()
      }
    }

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
