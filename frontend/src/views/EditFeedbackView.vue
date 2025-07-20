<template>
  <div class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Edit Feedback</h1>
            <p class="mt-1 text-sm text-gray-600">
              Update feedback for {{ feedback?.employee?.name }}
            </p>
          </div>
          <router-link
            to="/feedback"
            class="btn-secondary"
          >
            <ArrowLeftIcon class="h-4 w-4 mr-2" />
            Back to Feedback
          </router-link>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="card border-red-200 bg-red-50">
        <div class="card-body">
          <div class="flex items-center">
            <ExclamationTriangleIcon class="h-5 w-5 text-red-400 mr-2" />
            <p class="text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Edit Form -->
      <div v-else-if="feedback" class="card">
        <div class="card-header">
          <h2 class="text-lg font-medium text-gray-900">Feedback Details</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Employee (Read-only) -->
            <div>
              <label class="label">Employee</label>
              <div class="input bg-gray-50 text-gray-700">
                {{ feedback.employee.name }} ({{ feedback.employee.email }})
              </div>
            </div>

            <!-- Strengths -->
            <div>
              <label for="strengths" class="label">Strengths</label>
              <textarea
                id="strengths"
                v-model="form.strengths"
                rows="4"
                class="input"
                placeholder="Describe the employee's key strengths and positive contributions..."
                required
              ></textarea>
            </div>

            <!-- Areas to Improve -->
            <div>
              <label for="areas_to_improve" class="label">Areas to Improve</label>
              <textarea
                id="areas_to_improve"
                v-model="form.areas_to_improve"
                rows="4"
                class="input"
                placeholder="Suggest specific areas where the employee can grow and improve..."
                required
              ></textarea>
            </div>

            <!-- Sentiment -->
            <div>
              <label class="label">Overall Sentiment</label>
              <div class="mt-2 space-y-2">
                <label class="flex items-center">
                  <input
                    v-model="form.sentiment"
                    type="radio"
                    value="positive"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                  />
                  <span class="ml-2 text-sm text-gray-700 flex items-center">
                    <span class="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                    Positive
                  </span>
                </label>
                <label class="flex items-center">
                  <input
                    v-model="form.sentiment"
                    type="radio"
                    value="neutral"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                  />
                  <span class="ml-2 text-sm text-gray-700 flex items-center">
                    <span class="w-3 h-3 bg-yellow-500 rounded-full mr-2"></span>
                    Neutral
                  </span>
                </label>
                <label class="flex items-center">
                  <input
                    v-model="form.sentiment"
                    type="radio"
                    value="negative"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                  />
                  <span class="ml-2 text-sm text-gray-700 flex items-center">
                    <span class="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                    Negative
                  </span>
                </label>
              </div>
            </div>

            <!-- Tags -->
            <div>
              <label for="tags" class="label">Tags (Optional)</label>
              <input
                id="tags"
                v-model="tagsInput"
                type="text"
                class="input"
                placeholder="Enter tags separated by commas (e.g., leadership, communication, teamwork)"
              />
              <p class="mt-1 text-sm text-gray-500">
                Separate multiple tags with commas
              </p>
            </div>

            <!-- Anonymous Option -->
            <div class="flex items-center">
              <input
                id="is_anonymous"
                v-model="form.is_anonymous"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="is_anonymous" class="ml-2 block text-sm text-gray-700">
                Submit as anonymous feedback
              </label>
            </div>

            <!-- Form Actions -->
            <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
              <router-link
                to="/feedback"
                class="btn-secondary"
              >
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="isSubmitting"
                class="btn-primary"
              >
                <span v-if="isSubmitting" class="mr-2">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block"></div>
                </span>
                {{ isSubmitting ? 'Updating...' : 'Update Feedback' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Feedback History -->
      <div v-if="feedback?.employee_comment" class="mt-6 card">
        <div class="card-header">
          <h3 class="text-lg font-medium text-gray-900">Employee Response</h3>
        </div>
        <div class="card-body">
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-gray-700">{{ feedback.employee_comment }}</p>
            <p class="text-sm text-gray-500 mt-2">
              Acknowledged on {{ formatDate(feedback.acknowledged_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import apiService from '@/services/api'
import type { Feedback, FeedbackUpdate } from '@/types'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoading = ref(true)
const isSubmitting = ref(false)
const error = ref('')
const feedback = ref<Feedback | null>(null)

const form = reactive({
  strengths: '',
  areas_to_improve: '',
  sentiment: 'positive' as 'positive' | 'neutral' | 'negative',
  is_anonymous: false
})

const tagsInput = ref('')

const tags = computed(() => {
  return tagsInput.value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0)
})

const fetchFeedback = async () => {
  try {
    isLoading.value = true
    const feedbackId = parseInt(route.params.id as string)
    
    if (isNaN(feedbackId)) {
      error.value = 'Invalid feedback ID'
      return
    }

    feedback.value = await apiService.getFeedback(feedbackId)
    
    // Populate form with existing data
    form.strengths = feedback.value.strengths
    form.areas_to_improve = feedback.value.areas_to_improve
    form.sentiment = feedback.value.sentiment
    form.is_anonymous = feedback.value.is_anonymous
    tagsInput.value = feedback.value.tags.join(', ')
    
  } catch (err: any) {
    console.error('Failed to fetch feedback:', err)
    error.value = err.response?.data?.detail || 'Failed to load feedback'
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  try {
    isSubmitting.value = true
    
    const updateData: FeedbackUpdate = {
      strengths: form.strengths,
      areas_to_improve: form.areas_to_improve,
      sentiment: form.sentiment,
      tags: tags.value,
      is_anonymous: form.is_anonymous
    }

    await apiService.updateFeedback(feedback.value!.id, updateData)
    
    // Redirect back to feedback list with success message
    router.push({
      path: '/feedback',
      query: { updated: 'true' }
    })
    
  } catch (err: any) {
    console.error('Failed to update feedback:', err)
    error.value = err.response?.data?.detail || 'Failed to update feedback'
  } finally {
    isSubmitting.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  // Check if user is a manager
  if (!authStore.isManager) {
    router.push('/feedback')
    return
  }
  
  fetchFeedback()
})
</script>
