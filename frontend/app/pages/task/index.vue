<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { columns } from './components/columns'
import DataTable from './components/DataTable.vue'
import { Button } from '@/components/ui/button'
import { useRouter, useState } from '#imports' // if Nuxt 3; if plain Vue, remove useState and replace with your store

// ===== USER INFORMATION =====
const userData = useState<any>('userData', () => ({} as any))
const USER_ID = computed<string | null>(() => userData.value?.user?.id ?? null)
const role = computed(() => userData.value?.user?.role)
const name = computed(() => userData.value?.user?.name)

const router = useRouter()

// ===== API Configuration =====
const API_BASE_URL = 'http://localhost:4000'

// ===== State =====
const tasks = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// ===== Helpers =====
const normalizeRow = (item: any): any => {
  const t = item?.task ?? item ?? {}
  // Some services put schedule data under schedule.data, some directly under schedule
  const s = item?.schedule?.data ?? item?.schedule ?? null

  return {
    // Core task fields (lifted)
    id: t.id ?? null,
    title: t.name ?? '',
    parentTaskId: t.parentTaskId ?? null,
    priority: t.priorityLabel ?? null,

    // Joined/derived
    schedule: s,
    status: s?.status ?? null,

    // Flatten subtasks recursively in a field (we'll decide whether to expand them)
    subtasks: Array.isArray(item?.subtasks)
      ? item.subtasks.map(normalizeRow)
      : []
  }
}

// ===== Methods =====
const loadTasks = async () => {
  // Guard against missing user id
  if (!USER_ID.value) {
    console.warn('[Tasks] USER_ID not ready yet; aborting loadTasks for now.')
    return
  }

  loading.value = true
  error.value = null

  console.log('=== LOADING TASKS ===')
  console.log('Current USER_ID:', USER_ID.value)
  console.log('API URL:', `${API_BASE_URL}/tasks/user/${USER_ID.value}`)

  try {
    const response = await $fetch(`${API_BASE_URL}/tasks/user/${USER_ID.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })

    console.log('✅ Tasks API Response:', response)

    // Handle different response structures
    let taskList: any[] = []
    if (Array.isArray(response)) {
      taskList = response
    } else if (Array.isArray(response?.tasks)) {
      taskList = response.tasks
    } else if (Array.isArray(response?.data)) {
      taskList = response.data
    } else if (Array.isArray(response?.result)) {
      taskList = response.result
    } else if (Array.isArray(response?.items)) {
      taskList = response.items
    } else {
      // If direct object with a single task root
      taskList = [response].filter(Boolean)
    }

    console.log('📋 Raw taskList:', taskList)

    // Normalize the tasks
    const normalized = taskList.map(normalizeRow)

    console.log('📊 Normalized tasks sample:', normalized.slice(0, 2))
    console.log('📊 ParentTaskId values:', normalized.map(t => ({ id: t.id, title: t.title, parentTaskId: t.parentTaskId })))

    // Filter to only show top-level tasks (without parentTaskId)
    tasks.value = normalized.filter(task => !task.parentTaskId)
    
    console.log('✅ Final filtered rows (top-level only):', tasks.value)
  } catch (e: any) {
    console.error('❌ Error loading tasks:', e)
    error.value = e?.data?.message || e?.message || 'Failed to load tasks'
  } finally {
    loading.value = false
    console.log('===================')
  }
}

const handleCreateTask = () => {
  router.push('/task/create')
}

const handleRefresh = () => {
  loadTasks()
}

// ===== Lifecycle =====
// Use a watcher so we only fetch once USER_ID is ready (SSR-safe)
watch(
  () => USER_ID.value,
  (val, oldVal) => {
    if (val && val !== oldVal) loadTasks()
  },
  { immediate: true }
)
</script>

<template>
  <div class="container mx-auto py-10 px-3">
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div class="w-full sm:w-auto">
          <div class="flex items-center gap-3 mb-1">
            <h1 class="text-3xl font-bold tracking-tight">Tasks</h1>
            <button
              @click="handleRefresh"
              :disabled="loading"
              class="p-1.5 rounded-md hover:bg-muted transition-colors disabled:opacity-50"
              title="Refresh tasks"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :class="{ 'animate-spin': loading }"
              >
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
                <path d="M16 16h5v5"/>
              </svg>
            </button>
          </div>
          <p class="text-muted-foreground w-full sm:w-auto">
            {{ name ? `Welcome, ${name}` : 'Manage your tasks and view their details' }}
            <span v-if="tasks.length > 0" class="ml-1">
              • {{ tasks.length }} task{{ tasks.length !== 1 ? 's' : '' }}
            </span>
          </p>
        </div>

        <div class="hidden sm:block">
          <Button @click="handleCreateTask">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="mr-2">
              <path d="M5 12h14"/>
              <path d="M12 5v14"/>
            </svg>
            Create Task
          </Button>
        </div>
      </div>

      <!-- Error -->
      <div v-if="error" class="rounded-lg border border-destructive/50 bg-destructive/10 p-4">
        <div class="flex items-start gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
               viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
               class="text-destructive mt-0.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" x2="12" y1="8" y2="12"/>
            <line x1="12" x2="12.01" y1="16" y2="16"/>
          </svg>
          <div class="flex-1">
            <h3 class="font-semibold text-destructive">Error Loading Tasks</h3>
            <p class="text-sm text-muted-foreground mt-1">{{ error }}</p>
            <Button variant="outline" size="sm" class="mt-3" @click="handleRefresh">
              Try Again
            </Button>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading && tasks.length === 0" class="space-y-3">
        <div class="h-12 bg-muted rounded-lg animate-pulse"></div>
        <div class="h-64 bg-muted rounded-lg animate-pulse"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="!loading && tasks.length === 0 && !error"
           class="rounded-lg border border-dashed p-12 text-center">
        <div class="mx-auto flex max-w-[420px] flex-col items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48"
               viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
               class="text-muted-foreground/50 mb-4">
            <rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
          </svg>
          <h3 class="text-xl font-semibold mb-2">No tasks yet</h3>
          <p class="text-sm text-muted-foreground mb-6">Get started by creating your first task</p>
          <Button @click="handleCreateTask">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="mr-2">
              <path d="M5 12h14"/>
              <path d="M12 5v14"/>
            </svg>
            Create Your First Task
          </Button>
        </div>
      </div>

      <!-- Table -->
      <DataTable v-else-if="!loading && tasks.length > 0" :data="tasks" :columns="columns" />

      <!-- Mobile create -->
      <div class="block sm:hidden mt-4">
        <Button class="w-full" @click="handleCreateTask">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
               viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
               class="mr-2">
            <path d="M5 12h14"/>
            <path d="M12 5v14"/>
          </svg>
          Create Task
        </Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}
.animate-spin { animation: spin 1s linear infinite; }
</style>