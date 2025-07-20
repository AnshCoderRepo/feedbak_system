import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginCredentials, RegisterData } from '@/types'
import apiService from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isManager = computed(() => user.value?.role === 'manager')
  const isEmployee = computed(() => user.value?.role === 'employee')

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('auth_token', newToken)
  }

  const clearToken = () => {
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const login = async (credentials: LoginCredentials) => {
    try {
      loading.value = true
      error.value = null
      
      const authResponse = await apiService.login(credentials)
      setToken(authResponse.access_token)
      
      // Get user data after successful login
      const userData = await apiService.getUserProfile()
      user.value = userData
      
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      clearToken()
      user.value = null
      return false
    } finally {
      loading.value = false
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      loading.value = true
      error.value = null
      
      await apiService.register(userData)
      
      // Auto-login after successful registration
      const loginSuccess = await login({
        email: userData.email,
        password: userData.password,
      })
      
      return loginSuccess
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    clearToken()
    user.value = null
    error.value = null
  }

  const fetchCurrentUser = async () => {
    if (!token.value) return false
    
    try {
      loading.value = true
      const userData = await apiService.getUserProfile()
      user.value = userData
      return true
    } catch (err) {
      clearToken()
      user.value = null
      return false
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isManager,
    isEmployee,
    login,
    register,
    logout,
    fetchCurrentUser,
    clearError,
  }
})
