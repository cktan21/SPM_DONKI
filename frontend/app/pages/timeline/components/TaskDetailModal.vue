<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-xl">
      <!-- Fixed Header -->
      <div class="flex-shrink-0 bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between rounded-t-2xl">
        <h2 class="text-xl font-semibold text-slate-900">Task Details</h2>
        <button
          @click="$emit('close')"
          class="w-8 h-8 rounded-full hover:bg-slate-100 flex items-center justify-center transition-colors"
        >
          <svg class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Scrollable Content -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <div>
          <h3 class="text-2xl font-semibold text-slate-900">{{ task.name }}</h3>
          <p class="text-slate-500 mt-1">{{ task.project.name }}</p>
        </div>

        <div class="flex items-center gap-3 flex-wrap">
          <span
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              getStatusBadgeClass(task.status)
            ]"
          >
            {{ task.status }}
          </span>
          <span class="px-3 py-1 rounded-full text-sm font-medium bg-slate-100 text-slate-700">
            Priority: {{ task.priorityLevel }}
          </span>
          <span v-if="task.label" class="px-3 py-1 rounded-full text-sm font-medium bg-purple-50 text-purple-700 capitalize">
            {{ task.label }}
          </span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs text-slate-500 mb-1">Start Date</p>
            <p class="font-medium text-slate-900">{{ formatDate(task.start) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs text-slate-500 mb-1">Deadline</p>
            <p class="font-medium text-slate-900">{{ formatDate(task.deadline) }}</p>
          </div>
        </div>

        <div v-if="task.desc">
          <h4 class="font-medium text-slate-900 mb-2">Description</h4>
          <p class="text-slate-600">{{ task.desc }}</p>
        </div>

        <div v-if="task.notes">
          <h4 class="font-medium text-slate-900 mb-2">Notes</h4>
          <p class="text-slate-600">{{ task.notes }}</p>
        </div>

        <div v-if="task.collaborators && task.collaborators.length > 0">
          <h4 class="font-medium text-slate-900 mb-3">Collaborators</h4>
          <div class="flex flex-wrap gap-2">
            <div
              v-for="collab in task.collaborators"
              :key="collab.id"
              class="flex items-center gap-2 bg-slate-50 rounded-full px-3 py-2"
            >
              <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                {{ collab.name.charAt(0) }}
              </div>
              <span class="text-sm text-slate-700">{{ collab.name }}</span>
            </div>
          </div>
        </div>

        <div v-if="task.subtasks && task.subtasks.length > 0">
          <h4 class="font-medium text-slate-900 mb-3">Subtasks ({{ task.subtasks.length }})</h4>
          <div class="space-y-2">
            <div
              v-for="subtask in task.subtasks"
              :key="subtask.id"
              class="bg-slate-50 rounded-lg p-3"
            >
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <span class="text-sm text-slate-900">{{ subtask.name }}</span>
                <span
                  :class="[
                    'px-2 py-0.5 rounded-full text-xs font-medium',
                    getStatusBadgeClass(subtask.status)
                  ]"
                >
                  {{ subtask.status }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="task.messages && task.messages.length > 0">
          <h4 class="font-medium text-slate-900 mb-3">Messages ({{ task.messages.length }})</h4>
          <div class="space-y-3">
            <div
              v-for="message in task.messages"
              :key="message.id"
              class="bg-slate-50 rounded-lg p-3"
            >
              <div class="flex items-start gap-2 mb-1">
                <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium flex-shrink-0">
                  {{ message.sender_name.charAt(0) }}
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-slate-900">{{ message.sender_name }}</p>
                  <p class="text-xs text-slate-500">{{ formatDate(message.timestamp) }}</p>
                </div>
              </div>
              <p v-if="message.message" class="text-sm text-slate-700 ml-8 break-words">{{ message.message }}</p>
              <div v-if="message.attachments && message.attachments.length > 0" class="ml-8 mt-2">
                <div
                  v-for="attachment in message.attachments"
                  :key="attachment.url"
                  class="flex items-center gap-2 text-xs text-blue-600 hover:underline cursor-pointer"
                >
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                  <span class="truncate">{{ attachment.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate, getStatusBadgeClass } from '../utils.js'

defineProps({
  task: Object
})

defineEmits(['close'])
</script>