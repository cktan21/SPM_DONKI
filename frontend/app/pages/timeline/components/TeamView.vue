<template>
  <div>
    <!-- Empty State for Team View -->
    <div v-if="filteredTeamMembers.length === 0" class="text-center py-12">
      <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-slate-900 mb-1">No team members found</h3>
      <p class="text-slate-500">Try adjusting your filters</p>
    </div>

    <div v-else class="space-y-6">
      <div
        v-for="member in filteredTeamMembers"
        :key="member.id"
        class="border border-slate-200 rounded-lg overflow-hidden"
      >
        <div class="bg-slate-50 px-4 py-3 border-b border-slate-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-medium text-sm">
                {{ member.name.charAt(0) }}
              </div>
              <div>
                <h3 class="font-medium text-slate-900">{{ member.name }}</h3>
                <p class="text-xs text-slate-500">{{ member.tasks.length }} tasks</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs px-2 py-1 bg-red-50 text-red-700 rounded-full">
                {{ member.tasks.filter(t => t.status === 'overdue').length }} overdue
              </span>
            </div>
          </div>
        </div>
        
        <div class="p-4 space-y-3">
          <div
            v-for="task in member.tasks"
            :key="task.id"
            @click="$emit('selectTask', task)"
            class="cursor-pointer bg-slate-50 rounded-lg p-3 hover:bg-slate-100 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1 min-w-0">
                <h4 class="font-medium text-slate-900 text-sm">{{ task.name }}</h4>
                <p class="text-xs text-slate-500 mt-1">{{ task.project.name }}</p>
                <div class="flex items-center gap-2 mt-2 flex-wrap">
                  <span
                    :class="[
                      'px-2 py-0.5 rounded-full text-xs font-medium',
                      getStatusBadgeClass(task.status)
                    ]"
                  >
                    {{ task.status }}
                  </span>
                  <span class="text-xs text-slate-500">Due: {{ formatDate(task.deadline) }}</span>
                </div>
              </div>
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold ml-3',
                  getPriorityColor(task.priorityLevel)
                ]"
              >
                {{ task.priorityLevel }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate, getStatusBadgeClass, getPriorityColor } from '../utils.js'

defineProps({
  filteredTeamMembers: Array
})

defineEmits(['selectTask'])
</script>