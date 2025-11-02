<template>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
    <div class="bg-white rounded-xl p-6 border border-slate-200">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-slate-500">Total Tasks</p>
          <p class="text-2xl font-semibold text-slate-900 mt-1">{{ stats.total }}</p>
        </div>
        <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
          <svg class="w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl p-6 border border-slate-200">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-slate-500">Ongoing</p>
          <p class="text-2xl font-semibold text-blue-600 mt-1">{{ stats.ongoing }}</p>
        </div>
        <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
          <svg class="w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl p-6 border border-slate-200">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-slate-500">Overdue</p>
          <p class="text-2xl font-semibold text-red-600 mt-1">{{ stats.overdue }}</p>
        </div>
        <div class="w-12 h-12 bg-red-50 rounded-full flex items-center justify-center">
          <svg class="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl p-6 border border-slate-200">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-slate-500">Completed</p>
          <p class="text-2xl font-semibold text-green-600 mt-1">{{ stats.done }}</p>
        </div>
        <div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center">
          <svg class="w-6 h-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stats: Object
})
</script>