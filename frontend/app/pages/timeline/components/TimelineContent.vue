<template>
  <div class="bg-white rounded-xl border border-slate-200 overflow-hidden mt-5">
    <!-- Timeline Header -->
    <div class="border-b border-slate-200 bg-slate-50 px-6 py-4">
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-slate-900">
          {{ currentView === 'personal' ? 'My Schedule' : 'Team Schedule' }}
        </h2>
        <div class="text-sm text-slate-500">
          {{ formatDateRange() }}
        </div>
      </div>
    </div>

    <!-- Timeline Content -->
    <div class="p-6">
      <!-- Personal View -->
      <div v-if="currentView === 'personal'">
        <!-- Empty State -->
        <div v-if="filteredTasks.length === 0" class="text-center py-12">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-slate-900 mb-1">No tasks found</h3>
          <p class="text-slate-500">Try adjusting your filters</p>
        </div>

        <!-- Timeline View Toggle -->
        <div v-else>
          <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <button
                @click="timelineViewMode = 'stepper'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
                  timelineViewMode === 'stepper'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300'
                ]"
              >
                Timeline View
              </button>
              <button
                @click="timelineViewMode = 'card'"
                :class="[
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
                  timelineViewMode === 'card'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300'
                ]"
              >
                Card View
              </button>
            </div>
          </div>

          <!-- Stepper View -->
          <TimelineStepperView 
            v-if="timelineViewMode === 'stepper'"
            :tasks="filteredTasks"
            @selectTask="$emit('selectTask', $event)"
          />

          <!-- Card View -->
          <TimelineCardView 
            v-else
            :tasks="filteredTasks"
            @selectTask="$emit('selectTask', $event)"
          />
        </div>
      </div>

      <!-- Team View -->
      <TeamView 
        v-else
        :filteredTeamMembers="filteredTeamMembers"
        @selectTask="$emit('selectTask', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TimelineStepperView from './TimelineStepperView.vue'
import TimelineCardView from './TimelineCardView.vue'
import TeamView from './TeamView.vue'

const props = defineProps({
  currentView: String,
  filteredTasks: Array,
  filteredTeamMembers: Array,
  selectedTimeRange: String
})

defineEmits(['selectTask'])

const timelineViewMode = ref('stepper')

const formatDateRange = () => {
  const now = new Date()
  if (props.selectedTimeRange === 'week') {
    const end = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
    return `${formatDate(now)} - ${formatDate(end)}`
  } else if (props.selectedTimeRange === 'month') {
    return now.toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })
  } else {
    const end = new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000)
    return `${formatDate(now)} - ${formatDate(end)}`
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>