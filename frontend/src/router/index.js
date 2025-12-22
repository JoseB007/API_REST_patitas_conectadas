import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'
import MascotasView from '../views/MascotasView.vue'
import MascotaDetailView from '../views/MascotaDetailView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/mascotas',
      name: 'mascotas',
      component: MascotasView,
    },
    {
      path: '/mascotas/:uuid',
      name: 'mascota-detail',
      component: MascotaDetailView,
    }
  ]
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Verificar si la ruta requiere autenticación
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Si el usuario no está autenticado, redirigir a login
    if (!authStore.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // Guardar la ruta destino para redirigir después del login
      })
    } else {
      next() // Continuar la navegación
    }
  } else {
    next() // Continuar la navegación si no requiere autenticación
  }
})

export default router
