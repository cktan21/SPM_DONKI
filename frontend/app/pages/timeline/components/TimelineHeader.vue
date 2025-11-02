<template>
  <div class="bg-white border-b border-slate-200 sticky top-0 z-50 backdrop-blur-lg bg-white/80">
    <div class="max-w-[1400px] mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold text-slate-900">Timeline</h1>
          <p class="text-sm text-slate-500 mt-1">
            {{ userData.user_name }} • {{ userData.user_role }} • {{ userData.user_dept }}
          </p>
        </div>
        
        <div class="flex items-center gap-3">
          <!-- View Toggle -->
          <div class="bg-slate-100 rounded-lg p-1 flex items-center">
            <button
              v-for="view in viewModes"
              :key="view.value"
              @click="$emit('update:currentView', view.value)"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-all',
                currentView === view.value
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              {{ view.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- Filters Row -->
      <div class="flex items-center gap-3 mt-4 flex-wrap">
        <!-- Project Filter (for My Schedule view) -->
        <div v-if="currentView === 'personal'" class="flex-1 min-w-[200px] max-w-[300px]">
          <select
            :value="selectedProject"
            @change="$emit('update:selectedProject', $event.target.value)"
            class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Projects</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>

        <!-- Team Member Filter (for Team view) -->
        <div v-if="currentView === 'team'" class="flex-1 min-w-[200px] max-w-[300px]">
          <select
            :value="selectedTeamMember"
            @change="$emit('update:selectedTeamMember', $event.target.value)"
            class="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Team Members</option>
            <option v-for="member in teamMembers" :key="member.id" :value="member.id">
              {{ member.name }}
            </option>
          </select>
        </div>

        <!-- Status Filter -->
        <select
          :value="filterStatus"
          @change="$emit('update:filterStatus', $event.target.value)"
          class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Status</option>
          <option value="to do">To Do</option>
          <option value="ongoing">Ongoing</option>
          <option value="done">Done</option>
          <option value="overdue">Overdue</option>
        </select>

        <!-- Priority Filter -->
        <select
          :value="filterPriority"
          @change="$emit('update:filterPriority', $event.target.value)"
          class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Priority</option>
          <option value="high">High (8-10)</option>
          <option value="medium">Medium (4-7)</option>
          <option value="low">Low (1-3)</option>
        </select>

        <!-- Time Range Selector -->
        <div class="flex items-center gap-2 ml-auto">
          <button
            v-for="range in timeRanges"
            :key="range.value"
            @click="$emit('update:selectedTimeRange', range.value)"
            :class="[
              'px-3 py-2 rounded-lg text-sm font-medium transition-all',
              selectedTimeRange === range.value
                ? 'bg-blue-500 text-white'
                : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300'
            ]"
          >
            {{ range.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  userData: Object,
  currentView: String,
  viewModes: Array,
  projects: Array,
  teamMembers: Array,
  selectedProject: String,
  selectedTeamMember: String,
  filterStatus: String,
  filterPriority: String,
  selectedTimeRange: String,
  timeRanges: Array
})

defineEmits([
  'update:currentView',
  'update:selectedProject',
  'update:selectedTeamMember',
  'update:filterStatus',
  'update:filterPriority',
  'update:selectedTimeRange'
])
</script>