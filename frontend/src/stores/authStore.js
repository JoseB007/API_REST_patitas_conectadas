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
        this.error = err.message || 'Error al iniciar sesión'
        this.isAuthenticated = false
        this.user = null
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
        // Limpiar estado
        this.user = null
        this.isAuthenticated = false
      } catch (err) {
        this.error = err.message || 'Error al cerrar sesión'
        throw err
      } finally {
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
        this.error = err.message || 'Error al obtener el usuario'
        this.isAuthenticated = false
        this.user = null
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})

