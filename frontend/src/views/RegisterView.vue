<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <router-link
            to="/login"
            class="font-medium text-primary-600 hover:text-primary-500"
          >
            sign in to existing account
          </router-link>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              id="name"
              v-model="form.name"
              name="name"
              type="text"
              required
              class="input mt-1"
              placeholder="Enter your full name"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="input mt-1"
              placeholder="Enter your email"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                required
                class="input mt-1"
                placeholder="Enter your password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-2 text-gray-500 hover:text-gray-900"
                @click="showPassword = !showPassword"
              >
                <svg
                  v-if="showPassword"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
            <div class="relative">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                name="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                autocomplete="new-password"
                required
                class="input mt-1"
                placeholder="Confirm your password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 px-2 text-gray-500 hover:text-gray-900"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <svg
                  v-if="showConfirmPassword"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
          
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">Role</label>
            <select
              id="role"
              v-model="form.role"
              name="role"
              required
              class="input mt-1"
            >
              <option value="">Select your role</option>
              <option value="manager">Manager</option>
              <option value="employee">Employee</option>
            </select>
          </div>
          
          <div v-if="form.role === 'employee'">
            <label for="manager" class="block text-sm font-medium text-gray-700">Manager</label>
            <select
              id="manager"
              v-model="form.manager_id"
              name="manager"
              required
              class="input mt-1"
            >
              <option value="">Select your manager</option>
              <option v-for="manager in managers" :key="manager.id" :value="manager.id">
                {{ manager.name }} ({{ manager.email }})
              </option>
            </select>
          </div>
        </div>

        <div v-if="authStore.error" class="rounded-md bg-danger-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ExclamationTriangleIcon class="h-5 w-5 text-danger-400" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-danger-800">
                {{ authStore.error }}
              </h3>
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-primary w-full"
          >
            <span v-if="authStore.loading" class="mr-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block"></div>
            </span>
            {{ authStore.loading ? 'Creating account...' : 'Create account' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import apiService from '@/services/api'
import type { User } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'employee' as 'manager' | 'employee',
  manager_id: null as number | null
})

const managers = ref<User[]>([])
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)

const fetchManagers = async () => {
  try {
    loading.value = true
    managers.value = await apiService.getManagers()
  } catch (error: any) {
    console.error('Failed to fetch managers:', error)
    // Don't throw the error, just set empty managers list
    managers.value = []
    // Optionally show a warning message
    if (error?.response?.status === 0 || error?.code === 'ERR_NETWORK') {
      console.warn('Backend server may not be running. Please start the backend server.')
    }
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  authStore.clearError()
  
  if (form.role === 'employee' && !form.manager_id) {
    authStore.error = 'Please select a manager'
    return
  }
  
  if (form.password !== form.confirmPassword) {
    authStore.error = 'Passwords do not match'
    return
  }
  
  // Prepare manager_id: undefined for managers, valid integer for employees
  const manager_id = form.role === 'manager' ? undefined : (form.manager_id || undefined)
  
  const success = await authStore.register({
    name: form.name,
    email: form.email,
    password: form.password,
    role: form.role as 'manager' | 'employee',
    manager_id: manager_id
  })
  
  if (success) {
    router.push('/dashboard')
  }
}

onMounted(() => {
  authStore.clearError()
  fetchManagers()
})
</script>
