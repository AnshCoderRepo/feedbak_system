<template>
  <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">Profile</h1>
        <p class="mt-1 text-sm text-gray-600">
          Your account information and role details
        </p>
      </div>

      <!-- Profile Card -->
      <div class="card">
        <div class="card-body">
          <div class="flex items-center space-x-6">
            <!-- Avatar -->
            <div class="flex-shrink-0">
              <div class="h-20 w-20 rounded-full bg-primary-100 flex items-center justify-center">
                <span class="text-2xl font-medium text-primary-700">
                  {{ getInitials(authStore.user?.name || '') }}
                </span>
              </div>
            </div>

            <!-- User Info -->
            <div class="flex-1">
              <h2 class="text-xl font-bold text-gray-900">
                {{ authStore.user?.name }}
              </h2>
              <p class="text-sm text-gray-600">
                {{ authStore.user?.email }}
              </p>
              <div class="mt-2 flex items-center space-x-2">
                <span
                  class="badge"
                  :class="{
                    'badge-success': authStore.isManager,
                    'badge-gray': authStore.isEmployee
                  }"
                >
                  {{ authStore.user?.role }}
                </span>
                <span v-if="authStore.isEmployee && authStore.user?.manager" class="text-sm text-gray-500">
                  Reports to: {{ authStore.user.manager.name }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Account Details -->
      <div class="mt-6 card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Account Details</h3>
        </div>
        <div class="card-body">
          <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
            <div>
              <dt class="text-sm font-medium text-gray-500">Full Name</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ authStore.user?.name }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Email Address</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ authStore.user?.email }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Role</dt>
              <dd class="mt-1 text-sm text-gray-900 capitalize">{{ authStore.user?.role }}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500">Member Since</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ formatDate(authStore.user?.created_at || '') }}
              </dd>
            </div>
            <div v-if="authStore.isEmployee && authStore.user?.manager" class="sm:col-span-2">
              <dt class="text-sm font-medium text-gray-500">Manager</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ authStore.user.manager.name }} ({{ authStore.user.manager.email }})
              </dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Role-specific Information -->
      <div v-if="authStore.isManager" class="mt-6 card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Manager Information</h3>
        </div>
        <div class="card-body">
          <div class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-3">
            <div class="text-center">
              <div class="text-2xl font-bold text-primary-600">{{ teamSize }}</div>
              <div class="text-sm text-gray-500">Team Members</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-success-600">{{ totalFeedback }}</div>
              <div class="text-sm text-gray-500">Feedback Given</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-warning-600">{{ recentFeedback }}</div>
              <div class="text-sm text-gray-500">This Month</div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="authStore.isEmployee" class="mt-6 card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Feedback Summary</h3>
        </div>
        <div class="card-body">
          <div class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-3">
            <div class="text-center">
              <div class="text-2xl font-bold text-primary-600">{{ totalFeedback }}</div>
              <div class="text-sm text-gray-500">Total Received</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-warning-600">{{ unacknowledgedFeedback }}</div>
              <div class="text-sm text-gray-500">Unacknowledged</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-success-600">{{ acknowledgedFeedback }}</div>
              <div class="text-sm text-gray-500">Acknowledged</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-6 flex justify-end">
        <button
          @click="handleLogout"
          class="btn-danger"
        >
          <ArrowRightOnRectangleIcon class="h-4 w-4 mr-2" />
          Sign Out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRightOnRectangleIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import apiService from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

// Stats
const teamSize = ref(0)
const totalFeedback = ref(0)
const recentFeedback = ref(0)
const unacknowledgedFeedback = ref(0)
const acknowledgedFeedback = ref(0)

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const fetchStats = async () => {
  try {
    if (authStore.isManager) {
      const [teamMembers, dashboard] = await Promise.all([
        apiService.getTeamMembers(),
        apiService.getManagerDashboard()
      ])
      
      teamSize.value = teamMembers.length
      totalFeedback.value = dashboard.total_feedback
      
      // Calculate recent feedback (this month)
      const thisMonth = new Date()
      thisMonth.setDate(1)
      recentFeedback.value = dashboard.recent_feedback.filter(
        f => new Date(f.created_at) >= thisMonth
      ).length
      
    } else if (authStore.isEmployee) {
      const dashboard = await apiService.getEmployeeDashboard()
      
      totalFeedback.value = dashboard.total_feedback
      unacknowledgedFeedback.value = dashboard.unacknowledged_feedback
      acknowledgedFeedback.value = dashboard.total_feedback - dashboard.unacknowledged_feedback
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchStats()
})
</script>
