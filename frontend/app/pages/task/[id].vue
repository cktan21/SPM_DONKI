<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SubtaskItem from './components/SubtaskItem.vue'


// --- Setup ---
const route = useRoute()
const router = useRouter()
const taskId = computed(() => route.params.id as string)

const task = ref<any>(null)  // Main task object
const loading = ref(false)
const error = ref<string | null>(null)

// --- Fetch function ---
const fetchTask = async () => {
  try {
    loading.value = true
    error.value = null

    const response = await fetch(`http://127.0.0.1:4000/tasks/${taskId.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })

    if (!response.ok) throw new Error(`Server returned ${response.status}`)

    const data = await response.json()

    // Normalize single task response
    task.value = data.task
    task.value.schedule = data.schedule?.data || null
    task.value.project = data.task.project || null
    task.value.subtasks = data.subtasks || [] // Optional subtask list
    task.value.metadata = data.metadata || {}

  } catch (err: any) {
    error.value = err.message || 'Failed to load task'
  } finally {
    loading.value = false
  }
}

onMounted(fetchTask)
</script>

<template>
  <div class="container mx-auto py-10 space-y-6">
    <!-- Back Button -->
    <button 
      @click="router.back()"
      class="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
           viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
           class="mr-2">
        <path d="m15 18-6-6 6-6" />
      </svg>
      Back to tasks
    </button>

    <!-- Loading / Error -->
    <div v-if="loading" class="text-muted-foreground">Loading task details...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <!-- Main Task -->
    <div v-else-if="task" class="space-y-6">
      <!-- Metadata -->
      <div class="rounded-lg border bg-card p-6">
        <h2 class="text-lg font-semibold mb-2">Metadata</h2>
        <p>User ID: {{ task.user_id ?? 'N/A' }}</p>
        <p>Retrieved At: {{ task.metadata?.retrieved_at ? new Date(task.metadata.retrieved_at).toLocaleString() : 'N/A' }}</p>
        <p>Total Subtasks: {{ task.subtasks.length }}</p>
      </div>

      <!-- Task Info -->
      <div class="rounded-lg border bg-card p-6">
        <h1 class="text-3xl font-bold mb-2">{{ task.name }}</h1>
        <p>Task ID: {{ task.id }}</p>
        <p>Description: {{ task.desc ?? 'N/A' }}</p>
        <p>Notes: {{ task.notes ?? 'N/A' }}</p>
        <p>Priority: {{ task.priorityLabel ?? 'N/A' }} ({{ task.priorityLevel ?? 'N/A' }})</p>
        <p>Collaborators: {{ task.collaborators?.length ? task.collaborators.join(', ') : 'None' }}</p>

        <!-- Schedule -->
        <div v-if="task.schedule">
          <h3 class="font-semibold mt-4">Schedule</h3>
          <p>Status: {{ task.schedule.status ?? 'N/A' }}</p>
          <p>Deadline: {{ task.schedule.deadline ? new Date(task.schedule.deadline).toLocaleString() : 'N/A' }}</p>
        </div>

        <!-- Project -->
        <div v-if="task.project">
          <h3 class="font-semibold mt-4">Project</h3>
          <p>Project Name: {{ task.project.name ?? 'Unavailable' }}</p>
          <p>Project ID: {{ task.project.id ?? 'N/A' }}</p>
        </div>

        <!-- Subtasks -->
        <div v-if="task.subtasks?.length" class="mt-6">
          <h3 class="text-lg font-semibold mb-2">Subtasks</h3>
          <SubtaskItem
            v-for="sub in task.subtasks"
            :key="sub.id"
            :subtask="sub"
          />
        </div>
      </div>
    </div>

    <!-- No Data -->
    <div v-else class="text-muted-foreground">No task data found.</div>
  </div>
</template>
