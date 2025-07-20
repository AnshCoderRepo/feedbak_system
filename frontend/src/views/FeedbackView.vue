<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ authStore.isManager ? 'Feedback Given' : 'My Feedback' }}
            </h1>
            <p class="mt-1 text-sm text-gray-600">
              {{ authStore.isManager 
                ? 'Feedback you have provided to your team members' 
                : 'Feedback received from your manager' 
              }}
            </p>
          </div>
          <router-link
            v-if="authStore.isManager"
            to="/feedback/create"
            class="btn-primary"
          >
            <PlusIcon class="h-4 w-4 mr-2" />
            Give Feedback
          </router-link>
        </div>
      </div>

      <!-- Filters -->
      <div class="mb-6 flex flex-wrap gap-4">
        <select
          v-model="selectedSentiment"
          class="input w-auto"
        >
          <option value="">All Sentiments</option>
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>
        
        <select
          v-if="authStore.isEmployee"
          v-model="selectedAcknowledged"
          class="input w-auto"
        >
          <option value="">All Feedback</option>
          <option value="true">Acknowledged</option>
          <option value="false">Unacknowledged</option>
        </select>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Feedback List -->
      <div v-else-if="filteredFeedback.length > 0" class="space-y-6">
        <div
          v-for="feedback in filteredFeedback"
          :key="feedback.id"
          class="card"
        >
          <div class="card-body">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-3">
                  <h3 class="text-lg font-medium text-gray-900">
                    {{ authStore.isManager 
                      ? `Feedback for ${feedback.employee?.name}` 
                      : `From ${feedback.manager?.name}` 
                    }}
                  </h3>
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
                  <span v-if="authStore.isEmployee && !feedback.acknowledged" class="badge badge-warning">
                    Unacknowledged
                  </span>
                </div>
                
                <div class="space-y-4">
                  <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Strengths</h4>
                    <p class="text-sm text-gray-900">{{ feedback.strengths }}</p>
                  </div>
                  
                  <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Areas to Improve</h4>
                    <p class="text-sm text-gray-900">{{ feedback.areas_to_improve }}</p>
                  </div>
                  
                  <div v-if="feedback.tags" class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in feedback.tags.split(',')"
                      :key="tag.trim()"
                      class="badge badge-gray"
                    >
                      {{ tag.trim() }}
                    </span>
                  </div>
                  
                  <div v-if="feedback.employee_comment" class="bg-gray-50 p-3 rounded-md">
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Employee Response</h4>
                    <p class="text-sm text-gray-900">{{ feedback.employee_comment }}</p>
                  </div>
                </div>
              </div>
              
              <div class="ml-4 flex-shrink-0">
                <div class="text-sm text-gray-500">
                  {{ formatDate(feedback.created_at) }}
                  <span v-if="feedback.updated_at && feedback.updated_at !== feedback.created_at">
                    (edited {{ formatDate(feedback.updated_at) }})
                  </span>
                </div>
                
                <div class="mt-3 flex flex-col space-y-2">
                  <!-- Manager actions -->
                  <button
                    v-if="authStore.isManager"
                    @click="editFeedback(feedback)"
                    class="btn-secondary text-xs"
                  >
                    <PencilIcon class="h-3 w-3 mr-1" />
                    Edit
                  </button>
                  
                  <!-- Employee actions -->
                  <template v-if="authStore.isEmployee">
                    <button
                      v-if="!feedback.acknowledged"
                      @click="acknowledgeFeedback(feedback.id)"
                      :disabled="acknowledging === feedback.id"
                      class="btn-success text-xs"
                    >
                      <CheckIcon class="h-3 w-3 mr-1" />
                      {{ acknowledging === feedback.id ? 'Acknowledging...' : 'Acknowledge' }}
                    </button>
                    
                    <button
                      v-if="!feedback.employee_comment"
                      @click="showCommentModal(feedback)"
                      class="btn-secondary text-xs"
                    >
                      <ChatBubbleLeftIcon class="h-3 w-3 mr-1" />
                      Add Comment
                    </button>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12">
        <ChatBubbleLeftRightIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">No feedback found</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ authStore.isManager 
            ? 'Start giving feedback to your team members.' 
            : 'Your manager will provide feedback here.' 
          }}
        </p>
        <div v-if="authStore.isManager" class="mt-6">
          <router-link to="/feedback/create" class="btn-primary">
            <PlusIcon class="h-4 w-4 mr-2" />
            Give Feedback
          </router-link>
        </div>
      </div>
    </div>

    <!-- Comment Modal -->
    <div
      v-if="showingCommentModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeCommentModal"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Add Your Comment</h3>
          <textarea
            v-model="commentText"
            rows="4"
            class="textarea w-full"
            placeholder="Share your thoughts on this feedback..."
          ></textarea>
          <div class="flex justify-end space-x-3 mt-4">
            <button @click="closeCommentModal" class="btn-secondary">
              Cancel
            </button>
            <button
              @click="submitComment"
              :disabled="!commentText.trim() || submittingComment"
              class="btn-primary"
            >
              {{ submittingComment ? 'Submitting...' : 'Submit Comment' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusIcon,
  PencilIcon,
  CheckIcon,
  ChatBubbleLeftIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import type { Feedback } from '@/types'
import apiService from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const feedback = ref<Feedback[]>([])
const selectedSentiment = ref('')
const selectedAcknowledged = ref('')
const acknowledging = ref<number | null>(null)

// Comment modal
const showingCommentModal = ref(false)
const selectedFeedback = ref<Feedback | null>(null)
const commentText = ref('')
const submittingComment = ref(false)

const filteredFeedback = computed(() => {
  let filtered = feedback.value

  if (selectedSentiment.value) {
    filtered = filtered.filter(f => f.sentiment === selectedSentiment.value)
  }

  if (selectedAcknowledged.value !== '') {
    const isAcknowledged = selectedAcknowledged.value === 'true'
    filtered = filtered.filter(f => f.acknowledged === isAcknowledged)
  }

  return filtered.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

const fetchFeedback = async () => {
  try {
    loading.value = true
    feedback.value = await apiService.getMyFeedback()
  } catch (error) {
    console.error('Failed to fetch feedback:', error)
  } finally {
    loading.value = false
  }
}

const acknowledgeFeedback = async (feedbackId: number) => {
  try {
    acknowledging.value = feedbackId
    const updatedFeedback = await apiService.acknowledgeFeedback(feedbackId)
    
    // Update the feedback in the list
    const index = feedback.value.findIndex(f => f.id === feedbackId)
    if (index !== -1) {
      feedback.value[index] = updatedFeedback
    }
  } catch (error) {
    console.error('Failed to acknowledge feedback:', error)
  } finally {
    acknowledging.value = null
  }
}

const showCommentModal = (feedbackItem: Feedback) => {
  selectedFeedback.value = feedbackItem
  commentText.value = ''
  showingCommentModal.value = true
}

const closeCommentModal = () => {
  showingCommentModal.value = false
  selectedFeedback.value = null
  commentText.value = ''
}

const submitComment = async () => {
  if (!selectedFeedback.value || !commentText.value.trim()) return

  try {
    submittingComment.value = true
    const updatedFeedback = await apiService.addEmployeeComment(
      selectedFeedback.value.id,
      commentText.value.trim()
    )
    
    // Update the feedback in the list
    const index = feedback.value.findIndex(f => f.id === selectedFeedback.value!.id)
    if (index !== -1) {
      feedback.value[index] = updatedFeedback
    }
    
    closeCommentModal()
  } catch (error) {
    console.error('Failed to submit comment:', error)
  } finally {
    submittingComment.value = false
  }
}

const editFeedback = (feedbackItem: Feedback) => {
  // Navigate to edit page (we'll implement this later)
  router.push(`/feedback/edit/${feedbackItem.id}`)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchFeedback()
})
</script>
