<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">
          {{ authStore.isManager ? 'Manager Dashboard' : 'My Feedback Dashboard' }}
        </h1>
        <p class="mt-1 text-sm text-gray-600">
          {{ authStore.isManager 
            ? 'Overview of your team and feedback activity' 
            : 'Track your feedback and professional development' 
          }}
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Manager Dashboard -->
      <div v-else-if="authStore.isManager && managerData" class="space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <UsersIcon class="h-8 w-8 text-primary-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Team Size</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ managerData.team_size }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <ChatBubbleLeftRightIcon class="h-8 w-8 text-success-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Feedback</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ managerData.total_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <FaceSmileIcon class="h-8 w-8 text-success-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Positive</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ managerData.positive_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <FaceFrownIcon class="h-8 w-8 text-warning-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Needs Attention</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ managerData.negative_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <div class="card-header">
            <h3 class="text-lg font-medium text-gray-900">Quick Actions</h3>
          </div>
          <div class="card-body">
            <div class="flex flex-wrap gap-3">
              <router-link to="/feedback/create" class="btn-primary">
                <PlusIcon class="h-4 w-4 mr-2" />
                Give Feedback
              </router-link>
              <router-link to="/team" class="btn-secondary">
                <UsersIcon class="h-4 w-4 mr-2" />
                View Team
              </router-link>
            </div>
          </div>
        </div>

        <!-- Recent Feedback -->
        <div class="card">
          <div class="card-header">
            <h3 class="text-lg font-medium text-gray-900">Recent Feedback</h3>
          </div>
          <div class="card-body">
            <div v-if="managerData.recent_feedback.length === 0" class="text-center py-6">
              <ChatBubbleLeftRightIcon class="mx-auto h-12 w-12 text-gray-400" />
              <h3 class="mt-2 text-sm font-medium text-gray-900">No feedback yet</h3>
              <p class="mt-1 text-sm text-gray-500">Get started by giving feedback to your team members.</p>
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="feedback in managerData.recent_feedback"
                :key="feedback.id"
                class="border-l-4 pl-4 py-2"
                :class="{
                  'border-success-400': feedback.sentiment === 'positive',
                  'border-warning-400': feedback.sentiment === 'neutral',
                  'border-danger-400': feedback.sentiment === 'negative'
                }"
              >
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium text-gray-900">
                    Feedback for {{ feedback.employee?.name }}
                  </p>
                  <span
                    class="badge"
                    :class="{
                      'badge-success': feedback.sentiment === 'positive',
                      'badge-warning': feedback.sentiment === 'neutral',
                      'badge-danger': feedback.sentiment === 'negative'
                    }"
                  >
                    {{ feedback.sentiment }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mt-1">{{ formatDate(feedback.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Employee Dashboard -->
      <div v-else-if="authStore.isEmployee && employeeData" class="space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <ChatBubbleLeftRightIcon class="h-8 w-8 text-primary-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Feedback</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ employeeData.total_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <ExclamationTriangleIcon class="h-8 w-8 text-warning-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Unacknowledged</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ employeeData.unacknowledged_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <FaceSmileIcon class="h-8 w-8 text-success-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Positive</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ employeeData.positive_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-body">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <FaceFrownIcon class="h-8 w-8 text-danger-600" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Areas to Improve</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ employeeData.negative_feedback }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Feedback -->
        <div class="card">
          <div class="card-header">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">Recent Feedback</h3>
              <router-link to="/feedback" class="text-sm text-primary-600 hover:text-primary-500">
                View all
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="employeeData.recent_feedback.length === 0" class="text-center py-6">
              <ChatBubbleLeftRightIcon class="mx-auto h-12 w-12 text-gray-400" />
              <h3 class="mt-2 text-sm font-medium text-gray-900">No feedback yet</h3>
              <p class="mt-1 text-sm text-gray-500">Your manager will provide feedback here.</p>
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="feedback in employeeData.recent_feedback"
                :key="feedback.id"
                class="border-l-4 pl-4 py-2"
                :class="{
                  'border-success-400': feedback.sentiment === 'positive',
                  'border-warning-400': feedback.sentiment === 'neutral',
                  'border-danger-400': feedback.sentiment === 'negative'
                }"
              >
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium text-gray-900">
                    From {{ feedback.manager?.name }}
                  </p>
                  <div class="flex items-center space-x-2">
                    <span
                      class="badge"
                      :class="{
                        'badge-success': feedback.sentiment === 'positive',
                        'badge-warning': feedback.sentiment === 'neutral',
                        'badge-danger': feedback.sentiment === 'negative'
                      }"
                    >
                      {{ feedback.sentiment }}
                    </span>
                    <span v-if="!feedback.acknowledged" class="badge badge-warning">
                      Unacknowledged
                    </span>
                  </div>
                </div>
                <p class="text-sm text-gray-600 mt-1">{{ formatDate(feedback.created_at) }}</p>
                <p class="text-sm text-gray-800 mt-2">{{ feedback.strengths.substring(0, 100) }}...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  UsersIcon,
  ChatBubbleLeftRightIcon,
  FaceSmileIcon,
  FaceFrownIcon,
  PlusIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import type { ManagerDashboard, EmployeeDashboard } from '@/types'
import apiService from '@/services/api'

const authStore = useAuthStore()
const loading = ref(true)
const managerData = ref<ManagerDashboard | null>(null)
const employeeData = ref<EmployeeDashboard | null>(null)

const fetchDashboardData = async () => {
  try {
    loading.value = true
    
    if (authStore.isManager) {
      managerData.value = await apiService.getManagerDashboard()
    } else if (authStore.isEmployee) {
      employeeData.value = await apiService.getEmployeeDashboard()
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchDashboardData()
})
</script>
