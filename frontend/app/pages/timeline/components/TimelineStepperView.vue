<template>
  <div class="space-y-8">
    <div
      v-for="(task, index) in tasks"
      :key="task.id"
      class="relative"
    >
      <!-- Timeline Line (connecting dot to next item) -->
      <div
        v-if="index < tasks.length - 1"
        class="absolute left-8 w-0.5 h-full -translate-x-1/2"
        :class="getStatusColor(task.status)"
      ></div>

      <div class="flex gap-8">
        <!-- Timeline Dot & Date -->
        <div class="flex flex-col items-center flex-shrink-0 w-36 py-2">
          <div
            :class="[
              'w-14 h-14 rounded-full flex items-center justify-center font-semibold text-white shadow-lg mb-3 relative z-10',
              getStatusColor(task.status)
            ]"
          >
            <svg v-if="task.status === 'done'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else-if="task.status === 'overdue'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <svg v-else-if="task.status === 'ongoing'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <svg v-else class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="text-center">
            <p class="text-sm font-medium text-slate-900">{{ formatDateShort(task.deadline) }}</p>
            <p class="text-xs text-slate-500 mt-1">{{ formatTime(task.deadline) }}</p>
          </div>
        </div>

        <!-- Task Card -->
        <div
          @click="$emit('selectTask', task)"
          class="flex-1 group cursor-pointer bg-white border border-slate-200 rounded-xl p-6 hover:shadow-lg hover:border-blue-300 transition-all"
        >
          <div class="flex items-start justify-between gap-6 mb-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 mb-2 flex-wrap">
                <h3 class="text-lg font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">
                  {{ task.name }}
                </h3>
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-xs font-medium',
                    getStatusBadgeClass(task.status)
                  ]"
                >
                  {{ task.status }}
                </span>
                <span
                  v-if="task.priorityLevel >= 8"
                  class="px-3 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700"
                >
                  High Priority
                </span>
              </div>
              <p class="text-sm font-medium text-slate-600 mb-3">{{ task.project.name }}</p>
              <p v-if="task.desc" class="text-sm text-slate-500 line-clamp-2 mb-3">{{ task.desc }}</p>
            </div>
            
            <!-- Priority Badge -->
            <div
              :class="[
                'w-14 h-14 rounded-xl flex flex-col items-center justify-center font-bold text-lg shadow-sm',
                getPriorityColor(task.priorityLevel)
              ]"
            >
              <span class="text-xs font-medium opacity-70">P</span>
              <span>{{ task.priorityLevel }}</span>
            </div>
          </div>

          <!-- Task Meta Info -->
          <div class="flex items-center gap-6 text-sm text-slate-600 flex-wrap mb-4">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>Start: {{ formatDate(task.start) }}</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Due: {{ formatDate(task.deadline) }}</span>
            </div>
            <div v-if="task.label" class="flex items-center gap-2">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <span class="capitalize">{{ task.label }}</span>
            </div>
          </div>

          <!-- Collaborators & Subtasks -->
          <div class="flex items-center gap-6 pt-4 border-t border-slate-100">
            <div v-if="task.collaborators && task.collaborators.length > 0" class="flex items-center gap-2">
              <div class="flex -space-x-2">
                <div
                  v-for="(collab, idx) in task.collaborators.slice(0, 3)"
                  :key="collab.id"
                  class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium border-2 border-white"
                  :title="collab.name"
                >
                  {{ collab.name.charAt(0) }}
                </div>
                <div
                  v-if="task.collaborators.length > 3"
                  class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 text-xs font-medium border-2 border-white"
                >
                  +{{ task.collaborators.length - 3 }}
                </div>
              </div>
              <span class="text-xs text-slate-500">{{ task.collaborators.length }} collaborator(s)</span>
            </div>
            
            <div v-if="task.subtasks && task.subtasks.length > 0" class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span>{{ task.subtasks.length }} subtask(s)</span>
            </div>

            <div v-if="task.messages && task.messages.length > 0" class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <span>{{ task.messages.length }} message(s)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate, formatDateShort, formatTime, getStatusColor, getStatusBadgeClass, getPriorityColor } from '../utils.js'

defineProps({
  tasks: Array
})

defineEmits(['selectTask'])
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>