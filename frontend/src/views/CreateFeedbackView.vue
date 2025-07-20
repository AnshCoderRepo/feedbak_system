<template>
  <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">Give Feedback</h1>
        <p class="mt-1 text-sm text-gray-600">
          Provide structured feedback to help your team member grow and develop.
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="card">
          <div class="card-body space-y-6">
            <!-- Employee Selection -->
            <div>
              <label for="employee" class="block text-sm font-medium text-gray-700">
                Team Member *
              </label>
              <select
                id="employee"
                v-model="form.employee_id"
                required
                class="input mt-1"
                :class="{ 'border-red-300': errors.employee_id }"
              >
                <option value="">Select a team member</option>
                <option
                  v-for="member in teamMembers"
                  :key="member.id"
                  :value="member.id"
                >
                  {{ member.name }} ({{ member.email }})
                </option>
              </select>
              <p v-if="errors.employee_id" class="mt-1 text-sm text-red-600">
                {{ errors.employee_id }}
              </p>
            </div>

            <!-- Sentiment -->
            <div>
              <label for="sentiment" class="block text-sm font-medium text-gray-700">
                Overall Sentiment *
              </label>
              <select
                id="sentiment"
                v-model="form.sentiment"
                required
                class="input mt-1"
                :class="{ 'border-red-300': errors.sentiment }"
              >
                <option value="">Select sentiment</option>
                <option value="positive">Positive - Great performance</option>
                <option value="neutral">Neutral - Meeting expectations</option>
                <option value="negative">Needs Improvement - Below expectations</option>
              </select>
              <p v-if="errors.sentiment" class="mt-1 text-sm text-red-600">
                {{ errors.sentiment }}
              </p>
            </div>

            <!-- Strengths -->
            <div>
              <label for="strengths" class="block text-sm font-medium text-gray-700">
                Strengths *
              </label>
              <textarea
                id="strengths"
                v-model="form.strengths"
                rows="4"
                required
                class="textarea mt-1"
                :class="{ 'border-red-300': errors.strengths }"
                placeholder="What are this person's key strengths? What are they doing well?"
              ></textarea>
              <p v-if="errors.strengths" class="mt-1 text-sm text-red-600">
                {{ errors.strengths }}
              </p>
              <p class="mt-1 text-sm text-gray-500">
                Be specific and provide examples where possible.
              </p>
            </div>

            <!-- Areas to Improve -->
            <div>
              <label for="areas_to_improve" class="block text-sm font-medium text-gray-700">
                Areas to Improve *
              </label>
              <textarea
                id="areas_to_improve"
                v-model="form.areas_to_improve"
                rows="4"
                required
                class="textarea mt-1"
                :class="{ 'border-red-300': errors.areas_to_improve }"
                placeholder="What areas could this person focus on for improvement? What specific actions would help?"
              ></textarea>
              <p v-if="errors.areas_to_improve" class="mt-1 text-sm text-red-600">
                {{ errors.areas_to_improve }}
              </p>
              <p class="mt-1 text-sm text-gray-500">
                Focus on actionable suggestions and growth opportunities.
              </p>
            </div>

            <!-- Tags -->
            <div>
              <label for="tags" class="block text-sm font-medium text-gray-700">
                Tags (Optional)
              </label>
              <input
                id="tags"
                v-model="form.tags"
                type="text"
                class="input mt-1"
                placeholder="e.g., communication, leadership, technical skills"
              />
              <p class="mt-1 text-sm text-gray-500">
                Separate multiple tags with commas. These help categorize feedback.
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
              <label for="is_anonymous" class="ml-2 block text-sm text-gray-900">
                Make this feedback anonymous
              </label>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="submitError" class="rounded-md bg-danger-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ExclamationTriangleIcon class="h-5 w-5 text-danger-400" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-danger-800">
                {{ submitError }}
              </h3>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3">
          <router-link to="/feedback" class="btn-secondary">
            Cancel
          </router-link>
          <button
            type="submit"
            :disabled="submitting"
            class="btn-primary"
          >
            <span v-if="submitting" class="mr-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white inline-block"></div>
            </span>
            {{ submitting ? 'Submitting...' : 'Submit Feedback' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import type { User, FeedbackCreate } from '@/types'
import apiService from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const teamMembers = ref<User[]>([])
const submitting = ref(false)
const submitError = ref('')

const form = ref<FeedbackCreate>({
  employee_id: 0,
  strengths: '',
  areas_to_improve: '',
  sentiment: '' as any,
  tags: '',
  is_anonymous: false
})

const errors = ref<Record<string, string>>({})

const validateForm = () => {
  errors.value = {}

  if (!form.value.employee_id) {
    errors.value.employee_id = 'Please select a team member'
  }

  if (!form.value.sentiment) {
    errors.value.sentiment = 'Please select a sentiment'
  }

  if (!form.value.strengths.trim()) {
    errors.value.strengths = 'Please provide strengths feedback'
  } else if (form.value.strengths.trim().length < 10) {
    errors.value.strengths = 'Please provide more detailed strengths feedback'
  }

  if (!form.value.areas_to_improve.trim()) {
    errors.value.areas_to_improve = 'Please provide areas to improve'
  } else if (form.value.areas_to_improve.trim().length < 10) {
    errors.value.areas_to_improve = 'Please provide more detailed improvement suggestions'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  try {
    submitting.value = true
    submitError.value = ''

    await apiService.createFeedback({
      ...form.value,
      strengths: form.value.strengths.trim(),
      areas_to_improve: form.value.areas_to_improve.trim(),
      tags: form.value.tags.trim() || undefined
    })

    // Redirect to feedback list with success message
    router.push('/feedback')
  } catch (error: any) {
    submitError.value = error.response?.data?.detail || 'Failed to submit feedback'
  } finally {
    submitting.value = false
  }
}

const fetchTeamMembers = async () => {
  try {
    teamMembers.value = await apiService.getTeamMembers()
  } catch (error) {
    console.error('Failed to fetch team members:', error)
    submitError.value = 'Failed to load team members'
  }
}

onMounted(() => {
  // Redirect if not a manager
  if (!authStore.isManager) {
    router.push('/dashboard')
    return
  }

  fetchTeamMembers()
})
</script>
