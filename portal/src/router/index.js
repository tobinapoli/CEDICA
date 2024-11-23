import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/contenido',
      name: 'contenido',
      component: () => import('../views/ContenidoView.vue'),
    },
    {
      path: '/show_contenido/:id',
      name: 'show_contenido',
      component: () => import('../views/ShowContenidoView.vue'),
    },
    {
      path: '/consulta',
      name: 'consulta',
      component: () => import ('../views/Consulta.vue'),
    },
  ],
})

export default router
