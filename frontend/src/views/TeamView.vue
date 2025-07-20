<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">My Team</h1>
            <p class="mt-1 text-sm text-gray-600">
              Overview of your team members and their feedback status
            </p>
          </div>
          <router-link to="/feedback/create" class="btn-primary">
            <PlusIcon class="h-4 w-4 mr-2" />
            Give Feedback
          </router-link>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Team Members -->
      <div v-else-if="teamMembers.length > 0" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="member in teamMembers"
          :key="member.id"
          class="card hover:shadow-lg transition-shadow duration-200"
        >
          <div class="card-body">
            <div class="flex items-center space-x-3 mb-4">
              <div class="flex-shrink-0">
                <div class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                  <span class="text-sm font-medium text-primary-700">
                    {{ getInitials(member.name) }}
                  </span>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ member.name }}
                </p>
                <p class="text-sm text-gray-500 truncate">
                  {{ member.email }}
                </p>
              </div>
            </div>

            <div class="space-y-3">
              <!-- Feedback Stats -->
              <div class="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div class="text-lg font-semibold text-gray-900">
                    {{ memberStats[member.id]?.total || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">Total Feedback</div>
                </div>
                <div>
                  <div class="text-lg font-semibold text-gray-900">
                    {{ memberStats[member.id]?.unacknowledged || 0 }}
                  </div>
                  <div class="text-xs text-gray-500">Unacknowledged</div>
                </div>
              </div>

              <!-- Sentiment Distribution -->
              <div v-if="memberStats[member.id]?.total > 0" class="space-y-2">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-gray-500">Sentiment</span>
                </div>
                <div class="flex space-x-1">
                  <div
                    class="h-2 bg-success-400 rounded-l"
                    :style="{ width: `${getSentimentPercentage(member.id, 'positive')}%` }"
                  ></div>
                  <div
                    class="h-2 bg-warning-400"
                    :style="{ width: `${getSentimentPercentage(member.id, 'neutral')}%` }"
                  ></div>
                  <div
                    class="h-2 bg-danger-400 rounded-r"
                    :style="{ width: `${getSentimentPercentage(member.id, 'negative')}%` }"
                  ></div>
                </div>
                <div class="flex justify-between text-xs text-gray-500">
                  <span>{{ memberStats[member.id]?.positive || 0 }} positive</span>
                  <span>{{ memberStats[member.id]?.negative || 0 }} needs work</span>
                </div>
              </div>

              <!-- Last Feedback -->
              <div v-if="memberStats[member.id]?.lastFeedback" class="text-xs text-gray-500">
                Last feedback: {{ formatDate(memberStats[member.id].lastFeedback) }}
              </div>
              <div v-else class="text-xs text-gray-500">
                No feedback given yet
              </div>
            </div>

            <!-- Actions -->
            <div class="mt-4 flex space-x-2">
              <button
                @click="giveFeedback(member)"
                class="btn-primary text-xs flex-1"
              >
                <PlusIcon class="h-3 w-3 mr-1" />
                Give Feedback
              </button>
              <button
                @click="viewFeedback(member)"
                class="btn-secondary text-xs flex-1"
              >
                <EyeIcon class="h-3 w-3 mr-1" />
                View History
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12">
        <UsersIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">No team members</h3>
        <p class="mt-1 text-sm text-gray-500">
          You don't have any team members assigned to you yet.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusIcon,
  EyeIcon,
  UsersIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import type { User, Feedback } from '@/types'
import apiService from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const teamMembers = ref<User[]>([])
const memberStats = ref<Record<number, {
  total: number
  positive: number
  neutral: number
  negative: number
  unacknowledged: number
  lastFeedback?: string
}>>({})

const fetchTeamData = async () => {
  try {
    loading.value = true
    
    // Fetch team members
    teamMembers.value = await apiService.getTeamMembers()
    
    // Fetch feedback stats for each member
    for (const member of teamMembers.value) {
      try {
        const feedback = await apiService.getEmployeeFeedback(member.id)
        
        memberStats.value[member.id] = {
          total: feedback.length,
          positive: feedback.filter(f => f.sentiment === 'positive').length,
          neutral: feedback.filter(f => f.sentiment === 'neutral').length,
          negative: feedback.filter(f => f.sentiment === 'negative').length,
          unacknowledged: feedback.filter(f => !f.acknowledged).length,
          lastFeedback: feedback.length > 0 
            ? feedback.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())[0].created_at
            : undefined
        }
      } catch (error) {
        console.error(`Failed to fetch feedback for ${member.name}:`, error)
        memberStats.value[member.id] = {
          total: 0,
          positive: 0,
          neutral: 0,
          negative: 0,
          unacknowledged: 0
        }
      }
    }
  } catch (error) {
    console.error('Failed to fetch team data:', error)
  } finally {
    loading.value = false
  }
}

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const getSentimentPercentage = (memberId: number, sentiment: 'positive' | 'neutral' | 'negative') => {
  const stats = memberStats.value[memberId]
  if (!stats || stats.total === 0) return 0
  
  const count = stats[sentiment]
  return Math.round((count / stats.total) * 100)
}

const giveFeedback = (member: User) => {
  router.push(`/feedback/create?employee=${member.id}`)
}

const viewFeedback = (member: User) => {
  router.push(`/feedback?employee=${member.id}`)
}

const formatDate = (dateString?: string | null) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

onMounted(() => {
  // Redirect if not a manager
  if (!authStore.isManager) {
    router.push('/dashboard')
    return
  }

  fetchTeamData()
})
</script>
