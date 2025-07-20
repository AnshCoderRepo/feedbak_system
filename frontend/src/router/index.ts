import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/feedback',
      name: 'Feedback',
      component: () => import('@/views/FeedbackView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/feedback/create',
      name: 'CreateFeedback',
      component: () => import('@/views/CreateFeedbackView.vue'),
      meta: { requiresAuth: true, requiresManager: true }
    },
    {
      path: '/feedback/edit/:id',
      name: 'EditFeedback',
      component: () => import('@/views/EditFeedbackView.vue'),
      meta: { requiresAuth: true, requiresManager: true }
    },
    {
      path: '/team',
      name: 'Team',
      component: () => import('@/views/TeamView.vue'),
      meta: { requiresAuth: true, requiresManager: true }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Try to fetch current user if we have a token but no user data
  if (authStore.token && !authStore.user) {
    await authStore.fetchCurrentUser()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
    return
  }

  // Check if route requires manager role
  if (to.meta.requiresManager && !authStore.isManager) {
    next('/dashboard')
    return
  }

  next()
})

export default router
