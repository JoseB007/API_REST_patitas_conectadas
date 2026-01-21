import { defineStore } from 'pinia'
import { login as authLogin, logout as authLogout, getCurrentUser } from '../services/authService.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null

      try {
        const response = await authLogin(credentials)
        // Actualizar estado con el usuario
        this.user = response.user || response
        this.isAuthenticated = true
        return response
      } catch (err) {
        // Si falla el login, nos aseguramos que el estado esté limpio
        this.isAuthenticated = false
        this.user = null
        this.error = err.message || 'Error al iniciar sesión'
        throw err
      } finally {
        this.loading = false
      }
    },

    async logout() {
      this.loading = true
      this.error = null

      try {
        await authLogout()
      } catch (err) {
        this.error = err.message || 'Error al cerrar sesión'
        // No lanzamos el error si queremos que el logout local proceda siempre suavemente,
        // pero para cumplir con api estándar, a veces se prefiere lanzar.
        // Sin embargo, el requisito dice "Limpiar estado".
        // Vamos a registrar el error pero permitir la limpieza en finally.
        console.error('Logout error:', err)
      } finally {
        // Limpiar estado siempre, haya funcionado o no la petición al backend
        this.user = null
        this.isAuthenticated = false
        this.loading = false
      }
    },

    async fetchUser() {
      this.loading = true
      this.error = null

      try {
        const user = await getCurrentUser()
        this.user = user
        this.isAuthenticated = true
        return user
      } catch (err) {
        // Si falla fetchUser (y el refresh automático de api.js también falló),
        // el usuario no está autenticado.
        this.isAuthenticated = false
        this.user = null
        this.error = err.message || 'Error al obtener el usuario'
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})

