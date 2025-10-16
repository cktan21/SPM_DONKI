<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// --- Setup ---
const route = useRoute()
const router = useRouter()
const taskId = computed(() => route.params.id as string)

const task = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const expandedSubtasks = ref<Set<string>>(new Set())

// Edit modes
const editingTask = ref(false)
const editingSubtask = ref<string | null>(null)

// Edit forms
const taskEditForm = ref<any>({})
const subtaskEditForm = ref<any>({})

const statusOptions = ['not started', 'ongoing', 'completed']

// --- API bases ---
const API_BASE_URL = 'http://localhost:4000'   // composite/gateway for reads+writes (main task + updates)
const TASKA_BASE_URL = 'http://localhost:5500' // ONLY for get-subtasks (ptid)

// ---------- Helpers ----------
const isUuid = (v: string) => typeof v === 'string' && v.trim().length === 36

const normalizeSchedule = (raw: any) => {
  if (!raw) return {}
  // allow { data: {...} } or direct object
  return raw?.data ?? raw
}

const normalizeTask = (x: any) => {
  if (!x) return null
  const schedule = normalizeSchedule(x?.schedule ?? {})
  const subtasks = Array.isArray(x?.subtasks) ? x.subtasks : []
  return {
    ...x,
    schedule,
    subtasks, // will be replaced after we fetch from /ptid
  }
}

// ——— Subtask normalization to your expected /ptid response ———
// Input example:
// {
//   "id": "...",
//   "name": "New Task Title",
//   "created_by_uid": "...",
//   "updated_timestamp": "...",
//   "parentTaskId": "3394...40d",
//   "collaborators": ["uuid", ...],
//   "pid": "...",
//   "desc": "Optional description",
//   "notes": "Optional notes",
//   "priorityLevel": 5,
//   "priorityLabel": "Medium"
// }
const normalizeSubtask = (x: any) => ({
  id: x?.id ?? '',
  name: x?.name ?? 'Untitled',
  desc: x?.desc ?? '',
  notes: x?.notes ?? '',
  priorityLevel: x?.priorityLevel ?? undefined,
  priorityLabel: x?.priorityLabel ?? '',
  // The /ptid payload does not include schedule;
  // keep UI happy with sensible defaults:
  status: x?.status ?? 'not started',
  deadline: x?.deadline ?? '',
  // Keep extra fields (may be useful later)
  parentTaskId: x?.parentTaskId ?? null,
  pid: x?.pid ?? null,
  collaborators: Array.isArray(x?.collaborators) ? x.collaborators : [],
  created_by_uid: x?.created_by_uid ?? null,
  updated_timestamp: x?.updated_timestamp ?? null,
})

// ---------- Fetchers ----------
const fetchMainTask = async (id: string) => {
  // Read main task from COMPOSITE (API_BASE_URL)
  const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
  if (!res.ok) throw new Error(`Task fetch failed (${res.status})`)
  const text = await res.text()
  if (!text) throw new Error('Empty response from /tasks/{id} (composite)')

  const data = JSON.parse(text)
  // Accept { task: {...} } or direct object
  const rawTask = data?.task ?? (data?.id ? data : null)
  return normalizeTask(rawTask)
}

const fetchSubtasks = async (id: string) => {
  // ONLY this call goes to TASKA_BASE_URL (/ptid)
  const res = await fetch(`${TASKA_BASE_URL}/ptid/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
  if (!res.ok) throw new Error(`Subtasks fetch failed (${res.status})`)
  const text = await res.text()
  if (!text) return []

  const data = JSON.parse(text)
  const list = Array.isArray(data?.tasks) ? data.tasks : (Array.isArray(data) ? data : [])
  return list.map(normalizeSubtask)
}

const fetchTask = async () => {
  const id = String(taskId.value || '').trim()
  if (!isUuid(id)) {
    error.value = 'Invalid task ID (must be a 36-char UUID)'
    return
  }

  try {
    loading.value = true
    error.value = null

    // Fetch main task (composite) then its subtasks (task MS) in parallel
    const [main, subs] = await Promise.all([fetchMainTask(id), fetchSubtasks(id)])

    if (!main) {
      error.value = 'Task not found'
      task.value = null
      return
    }

    task.value = {
      ...main,
      subtasks: subs
    }

    // Initialize edit form
    taskEditForm.value = {
      name: task.value?.name || '',
      desc: task.value?.desc || '',
      notes: task.value?.notes || '',
      priorityLabel: task.value?.priorityLabel || '',
      status: task.value?.schedule?.status || 'not started',
      deadline: task.value?.schedule?.deadline || ''
    }
  } catch (e: any) {
    console.error(e)
    error.value = e?.message || 'Failed to load task'
  } finally {
    loading.value = false
  }
}

// ---------- UI logic ----------
const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return 'N/A'
  }
}

const toggleSubtask = (subtaskId: string) => {
  if (expandedSubtasks.value.has(subtaskId)) {
    expandedSubtasks.value.delete(subtaskId)
  } else {
    expandedSubtasks.value.add(subtaskId)
  }
}

const startEditTask = () => {
  editingTask.value = true
  taskEditForm.value = {
    name: task.value?.name || '',
    desc: task.value?.desc || '',
    notes: task.value?.notes || '',
    priorityLabel: task.value?.priorityLabel || '',
    status: task.value?.schedule?.status || 'not started',
    deadline: task.value?.schedule?.deadline || ''
  }
}

const cancelEditTask = () => {
  editingTask.value = false
}

const saveTask = async () => {
  try {
    // Writes go to API_BASE_URL (composite)
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(taskEditForm.value)
    })
    if (!response.ok) throw new Error('Failed to update task')
    await fetchTask()
    editingTask.value = false
  } catch (err: any) {
    alert('Error updating task: ' + err.message)
  }
}

const startEditSubtask = (subtask: any) => {
  editingSubtask.value = subtask.id
  subtaskEditForm.value = {
    name: subtask.name || '',
    desc: subtask.desc || '',
    notes: subtask.notes || '',
    status: subtask.status || 'not started',
    deadline: subtask.deadline || '',
    priorityLabel: subtask.priorityLabel || ''
  }
}

const cancelEditSubtask = () => {
  editingSubtask.value = null
}

const saveSubtask = async (subtaskId: string) => {
  try {
    // Writes go to API_BASE_URL (composite)
    const response = await fetch(`${API_BASE_URL}/tasks/${subtaskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subtaskEditForm.value)
    })
    if (!response.ok) throw new Error('Failed to update subtask')
    await fetchTask()
    editingSubtask.value = null
  } catch (err: any) {
    alert('Error updating subtask: ' + err.message)
  }
}

const deleteSubtask = async (subtaskId: string) => {
  if (!confirm('Are you sure you want to delete this subtask?')) return
  try {
    // Writes go to API_BASE_URL (composite)
    const response = await fetch(`${API_BASE_URL}/tasks/${subtaskId}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!response.ok) throw new Error('Failed to delete subtask')
    await fetchTask()
  } catch (err: any) {
    alert('Error deleting subtask: ' + err.message)
  }
}

onMounted(fetchTask)
</script>

<template>
  <div class="container mx-auto py-10 space-y-6 max-w-5xl px-4">
    <!-- Back Button -->
    <button 
      @click="router.back()"
      class="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
           viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
           class="mr-2">
        <path d="m15 18-6-6 6-6" />
      </svg>
      Back to tasks
    </button>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-600">Loading task details...</div>
    
    <!-- Error -->
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <!-- Task Details -->
    <div v-else-if="task" class="space-y-6">
      <!-- Task Info Card -->
      <div class="rounded-lg border border-gray-200 bg-white p-6">
        <div class="flex items-start justify-between mb-4">
          <h1 v-if="!editingTask" class="text-3xl font-bold">{{ task.name || 'Untitled Task' }}</h1>
          <input 
            v-else
            v-model="taskEditForm.name"
            class="text-3xl font-bold border-b-2 border-blue-500 focus:outline-none w-full mr-4"
            placeholder="Task name"
          />
          
          <button 
            v-if="!editingTask"
            @click="startEditTask"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium"
          >
            Edit Task
          </button>
          <div v-else class="flex gap-2">
            <button 
              @click="saveTask"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm font-medium"
            >
              Save
            </button>
            <button 
              @click="cancelEditTask"
              class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition text-sm font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
        
        <div class="space-y-4 text-sm">
          <!-- Status and Deadline -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4 border-b border-gray-200">
            <div>
              <span class="font-medium block mb-1">Status:</span>
              <select 
                v-if="editingTask"
                v-model="taskEditForm.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option v-for="opt in statusOptions" :key="opt" :value="opt">{{ opt }}</option>
              </select>
              <span v-else class="inline-block px-3 py-1 rounded-full text-xs font-medium"
                    :class="{
                      'bg-green-100 text-green-800': task.schedule?.status === 'completed',
                      'bg-blue-100 text-blue-800': task.schedule?.status === 'ongoing',
                      'bg-gray-100 text-gray-800': task.schedule?.status === 'not started'
                    }">
                {{ task.schedule?.status || 'not started' }}
              </span>
            </div>
            
            <div>
              <span class="font-medium block mb-1">Deadline:</span>
              <input 
                v-if="editingTask"
                v-model="taskEditForm.deadline"
                type="datetime-local"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span v-else class="text-gray-700">{{ formatDate(task.schedule?.deadline) }}</span>
            </div>
          </div>

          <!-- Description -->
          <div>
            <span class="font-medium block mb-1">Description:</span>
            <textarea 
              v-if="editingTask"
              v-model="taskEditForm.desc"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Task description"
            ></textarea>
            <p v-else class="text-gray-700">{{ task.desc || 'N/A' }}</p>
          </div>

          <!-- Notes -->
          <div>
            <span class="font-medium block mb-1">Notes:</span>
            <textarea 
              v-if="editingTask"
              v-model="taskEditForm.notes"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Additional notes"
            ></textarea>
            <p v-else class="text-gray-700">{{ task.notes || 'N/A' }}</p>
          </div>

          <!-- Priority -->
          <div>
            <span class="font-medium">Priority:</span>
            <input 
              v-if="editingTask"
              v-model="taskEditForm.priorityLabel"
              class="ml-2 px-3 py-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g. High, Medium, Low"
            />
            <span v-else class="ml-2 text-gray-700">{{ task.priorityLabel || 'N/A' }}</span>
          </div>
        </div>
      </div>

      <!-- Subtasks Card -->
      <div v-if="task.subtasks && task.subtasks.length > 0" class="rounded-lg border border-gray-200 bg-white p-6">
        <h3 class="text-lg font-semibold mb-4">Subtasks ({{ task.subtasks.length }})</h3>
        <div class="space-y-3">
          <div 
            v-for="sub in task.subtasks" 
            :key="sub.id" 
            class="border border-gray-200 rounded-lg overflow-hidden"
          >
            <!-- Subtask Header -->
            <div class="p-4 hover:bg-gray-50 transition">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-2">
                    <button 
                      @click="toggleSubtask(sub.id)"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor"
                           stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                           :class="{ 'rotate-90': expandedSubtasks.has(sub.id) }"
                           class="transition-transform">
                        <path d="m9 18 6-6-6-6" />
                      </svg>
                    </button>
                    
                    <input 
                      v-if="editingSubtask === sub.id"
                      v-model="subtaskEditForm.name"
                      class="font-semibold text-base border-b-2 border-blue-500 focus:outline-none flex-1"
                      placeholder="Subtask name"
                    />
                    <p v-else class="font-semibold text-base">{{ sub.name }}</p>
                    
                    <select 
                      v-if="editingSubtask === sub.id"
                      v-model="subtaskEditForm.status"
                      class="px-2 py-1 border border-gray-300 rounded text-xs"
                    >
                      <option v-for="opt in statusOptions" :key="opt" :value="opt">{{ opt }}</option>
                    </select>
                    <span v-else class="px-2 py-1 rounded-full text-xs font-medium"
                          :class="{
                            'bg-green-100 text-green-800': sub.status === 'completed',
                            'bg-blue-100 text-blue-800': sub.status === 'ongoing',
                            'bg-gray-100 text-gray-800': sub.status === 'not started' || !sub.status
                          }">
                      {{ sub.status || 'not started' }}
                    </span>
                  </div>
                  
                  <div class="ml-8 text-sm text-gray-600">
                    <span class="font-medium">Deadline:</span>
                    <input 
                      v-if="editingSubtask === sub.id"
                      v-model="subtaskEditForm.deadline"
                      type="datetime-local"
                      class="ml-2 px-2 py-1 border border-gray-300 rounded text-xs"
                    />
                    <span v-else class="ml-2">{{ formatDate(sub.deadline) }}</span>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex gap-2 ml-4">
                  <template v-if="editingSubtask === sub.id">
                    <button 
                      @click="saveSubtask(sub.id)"
                      class="p-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
                      title="Save"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor"
                           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </button>
                    <button 
                      @click="cancelEditSubtask"
                      class="p-2 bg-gray-400 text-white rounded hover:bg-gray-500 transition"
                      title="Cancel"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor"
                           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" x2="6" y1="6" y2="18" />
                        <line x1="6" x2="18" y1="6" y2="18" />
                      </svg>
                    </button>
                  </template>
                  <template v-else>
                    <button 
                      @click="startEditSubtask(sub)"
                      class="p-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                      title="Edit"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor"
                           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" />
                      </svg>
                    </button>
                    <button 
                      @click="deleteSubtask(sub.id)"
                      class="p-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
                      title="Delete"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                           viewBox="0 0 24 24" fill="none" stroke="currentColor"
                           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 6h18" />
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                      </svg>
                    </button>
                  </template>
                </div>
              </div>
            </div>

            <!-- Expanded Details -->
            <div v-if="expandedSubtasks.has(sub.id)" class="px-4 pb-4 pt-2 bg-gray-50 border-t border-gray-200">
              <div class="ml-8 space-y-3 text-sm">
                <div v-if="editingSubtask === sub.id || sub.desc">
                  <span class="font-medium block mb-1">Description:</span>
                  <textarea 
                    v-if="editingSubtask === sub.id"
                    v-model="subtaskEditForm.desc"
                    rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Description"
                  ></textarea>
                  <p v-else class="text-gray-700">{{ sub.desc || 'N/A' }}</p>
                </div>
                
                <div v-if="editingSubtask === sub.id || sub.notes">
                  <span class="font-medium block mb-1">Notes:</span>
                  <textarea 
                    v-if="editingSubtask === sub.id"
                    v-model="subtaskEditForm.notes"
                    rows="2"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Notes"
                  ></textarea>
                  <p v-else class="text-gray-700">{{ sub.notes || 'N/A' }}</p>
                </div>
                
                <div v-if="sub.priorityLabel">
                  <span class="font-medium">Priority:</span>
                  <input 
                    v-if="editingSubtask === sub.id"
                    v-model="subtaskEditForm.priorityLabel"
                    class="ml-2 px-2 py-1 border border-gray-300 rounded"
                    placeholder="Priority"
                  />
                  <span v-else class="ml-2 text-gray-700">{{ sub.priorityLabel }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Subtasks -->
      <div v-else class="rounded-lg border border-dashed border-gray-300 p-8 text-center text-gray-500">
        No subtasks found for this task.
      </div>
    </div>

    <!-- No Data -->
    <div v-else class="text-gray-600">No task data found.</div>
  </div>
</template>

<style scoped>
.rotate-90 { transform: rotate(90deg); }
</style>
