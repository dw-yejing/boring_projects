import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/piano',
    name: 'Piano',
    component: () => import('@/components/Piano.vue')
  },
  {
    path: '/score',
    name: 'Score',
    component: () => import('@/components/Score.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
