<template>
  <div class="min-h-screen w-full bg-neutral-950 text-neutral-100 flex flex-col">
    <!-- ===== Top Header ===== -->
    <header class="w-full border-b border-neutral-800 bg-neutral-900/70 backdrop-blur sticky top-0 z-20">
      <div class="mx-auto max-w-7xl px-6 h-16 flex items-center justify-between">
        <h1 class="text-2xl font-semibold tracking-wide">ProjectName</h1>
        <button @click="loadTasks" class="px-3 py-1.5 rounded-lg bg-neutral-800 hover:bg-neutral-700 text-sm">
          Refresh
        </button>
      </div>
    </header>

    <!-- ===== Tasks Section ===== -->
    <main class="flex-1 w-full">
      <section class="mx-auto max-w-7xl px-6 py-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-lg font-semibold">Tasks</h2>
            <p class="text-sm text-neutral-400">ProjectName / Task list</p>
          </div>
          <button @click="ui.showCreate = true" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 font-medium">
            Create
          </button>
        </div>

        <div class="rounded-2xl border border-neutral-800 bg-neutral-900/60 p-4">
          <!-- Loading -->
          <div v-if="state.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="i in 6" :key="'sk' + i" class="h-32 rounded-xl bg-neutral-800 animate-pulse"></div>
          </div>

          <!-- Empty -->
          <div v-else-if="!state.tasks.length" class="h-40 grid place-items-center text-neutral-400">
            Select or create a task to view details.
          </div>

          <!-- Task grid -->
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <article v-for="t in state.tasks" :key="t.id"
              class="relative rounded-xl border border-neutral-800 bg-neutral-950/70 hover:bg-neutral-900/70 transition p-4">
              <div class="absolute right-3 top-3 flex items-center gap-1">
                <button @click="openEdit(t.id)" class="px-2 py-1 text-xs rounded-md bg-neutral-800 hover:bg-neutral-700"
                  title="Edit">
                  Edit
                </button>
              </div>

              <div class="mb-3">
                <div class="w-10 h-10 rounded-lg bg-neutral-800/70 grid place-items-center">
                  <div class="w-5 space-y-1">
                    <div class="h-0.5 bg-neutral-300/80"></div>
                    <div class="h-0.5 bg-neutral-300/80"></div>
                  </div>
                </div>
              </div>

              <h3 class="font-medium truncate">{{ t.name || 'Untitled Task' }}</h3>
              <p class="text-sm text-neutral-400 line-clamp-2 mt-1">{{ t.desc || '—' }}</p>
              <div class="mt-3 text-[11px] text-neutral-500">
                <span class="font-mono">{{ shortId(t.id) }}</span>
              </div>
            </article>
          </div>
        </div>
      </section>
    </main>

    <!-- ===== Create Modal (POST /createTask) ===== -->
    <div v-if="ui.showCreate" class="fixed inset-0 z-40 grid place-items-center bg-black/60 p-4"
      @click.self="ui.showCreate = false">
      <div class="w-full max-w-2xl rounded-2xl border border-neutral-800 bg-neutral-950 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Create Task</h3>
          <button @click="ui.showCreate = false" class="text-neutral-400 hover:text-neutral-200">✕</button>
        </div>

        <form @submit.prevent="createTask" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Name</label>
              <input v-model="formCreate.name"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500"
                required />
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">PID (Project ID)</label>
              <input v-model="formCreate.pid"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500"
                placeholder="optional" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Parent Task ID</label>
              <input v-model="formCreate.parentTaskId"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500"
                placeholder="optional" />
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Collaborators (CSV of UUIDs)</label>
              <input v-model="formCreate.collaboratorsCsv"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500"
                placeholder="id1,id2,..." />
            </div>
          </div>

          <div>
            <label class="block text-sm text-neutral-300 mb-1">Description</label>
            <textarea v-model="formCreate.desc" rows="3"
              class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500 resize-none" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Notes</label>
              <input v-model="formCreate.notes"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Schedule Status</label>
              <select v-model="formCreate.schedule.status"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500">
                <option value="">—</option>
                <option value="todo">todo</option>
                <option value="in_progress">in_progress</option>
                <option value="done">done</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Priority</label>
              <select v-model="formCreate.schedule.priority"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500">
                <option value="">—</option>
                <option value="low">low</option>
                <option value="medium">medium</option>
                <option value="high">high</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm text-neutral-300 mb-1">Deadline (ISO)</label>
            <input v-model="formCreate.schedule.deadline" type="datetime-local"
              class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
          </div>

          <div class="flex items-center justify-end gap-2 pt-2">
            <button type="button" @click="ui.showCreate = false"
              class="px-3 py-2 rounded-xl bg-neutral-800 hover:bg-neutral-700">Cancel</button>
            <button type="submit" :disabled="state.creating"
              class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-60">
              {{ state.creating ? 'Creating…' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ===== Edit Modal (GET /tasks/{id} then PUT /{id}) ===== -->
    <div v-if="ui.showEdit" class="fixed inset-0 z-40 grid place-items-center bg-black/60 p-4"
      @click.self="ui.showEdit = false">
      <div class="w-full max-w-2xl rounded-2xl border border-neutral-800 bg-neutral-950 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Edit Task</h3>
          <button @click="ui.showEdit = false" class="text-neutral-400 hover:text-neutral-200">✕</button>
        </div>

        <form @submit.prevent="saveEdit" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Name</label>
              <input v-model="formEdit.name"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500"
                required />
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">PID</label>
              <input v-model="formEdit.pid"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Parent Task ID</label>
              <input v-model="formEdit.parentTaskId"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Collaborators (CSV)</label>
              <input v-model="formEdit.collaboratorsCsv"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
            </div>
          </div>

          <div>
            <label class="block text-sm text-neutral-300 mb-1">Description</label>
            <textarea v-model="formEdit.desc" rows="3"
              class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500 resize-none" />
          </div>

          <div>
            <label class="block text-sm text-neutral-300 mb-1">Notes</label>
            <input v-model="formEdit.notes"
              class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Schedule Status</label>
              <select v-model="formEdit.schedule.status"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500">
                <option value="">—</option>
                <option value="todo">todo</option>
                <option value="in_progress">in_progress</option>
                <option value="done">done</option>
              </select>
            </div>
            <div>
              <label class="block text-sm text-neutral-300 mb-1">Deadline</label>
              <input v-model="formEdit.schedule.deadline" type="datetime-local"
                class="w-full rounded-xl border border-neutral-700 bg-neutral-900 px-3 py-2 outline-none focus:border-blue-500" />
            </div>
          </div>

          <div class="flex items-center justify-between pt-2">
            <button type="button" @click="confirmDelete" class="px-3 py-2 rounded-xl bg-red-600 hover:bg-red-500"
              :disabled="state.saving">
              Delete
            </button>
            <div class="flex items-center gap-2">
              <button type="button" @click="ui.showEdit = false"
                class="px-3 py-2 rounded-xl bg-neutral-800 hover:bg-neutral-700">
                Cancel
              </button>
              <button type="submit" :disabled="state.saving"
                class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-60">
                {{ state.saving ? 'Saving…' : 'Save' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, computed } from 'vue'
import axios from 'axios'

// ===== TESTING CONFIGURATION =====
const userData = useState<any>('userData', () => ({} as any))
const USER_ID = computed<string | null>(() => userData.value?.user?.id ?? null)
console.log('Using USER_ID:', USER_ID.value)
console.log('Using USER_ID:', USER_ID) // Debug log

// ===== SERVICE BASE URLS =====
const trackScheduleComposite = 'http://localhost:5600'
const TASKS_atomic = 'http://localhost:5500'
const PROJECTS_Atomic = 'http://localhost:5200'
const USERS_atomic = 'http://localhost:5700'


type Task = {
  id: string
  name?: string
  desc?: string
  notes?: string
  pid?: string
  parentTaskId?: string
  collaborators?: string[]
  updated_timestamp?: string
  created_by_uuid?: string
}

type Schedule = {
  status?: string
  deadline?: string
  priority?: string
}

// ===== axios points to the COMPOSITE (port 5600) =====
const api = axios.create({ baseURL: trackScheduleComposite })

const state = reactive({
  tasks: [] as Task[],
  loading: false,
  creating: false,
  saving: false,
  editingId: '' as string | '',
})

const ui = reactive({
  showCreate: false,
  showEdit: false,
})

const formCreate = reactive({
  name: '',
  desc: '',
  notes: '',
  pid: '',
  parentTaskId: '',
  collaboratorsCsv: '',
  schedule: { status: '', deadline: '', priority: '' } as Schedule,
})

const formEdit = reactive({
  name: '',
  desc: '',
  notes: '',
  pid: '',
  parentTaskId: '',
  collaboratorsCsv: '',
  schedule: { status: '', deadline: '' } as Schedule,
})

function shortId(id?: string) {
  if (!id) return ''
  return id.slice(0, 4) + '…' + id.slice(-4)
}

/** GET /tasks (for list) */
async function loadTasks() {
  try {
    const { data } = await api.get('/tasks')
    let list: any[] = []
    if (Array.isArray(data)) list = data
    else if (Array.isArray(data?.tasks)) list = data.tasks
    else if (Array.isArray(data?.data)) list = data.data
    else if (Array.isArray(data?.result)) list = data.result
    else if (Array.isArray(data?.items)) list = data.items
    state.tasks = list
  } catch (e: any) {
    if (e?.response) {
      console.error('Error loading tasks:', `status=${e.response.status}`, 'body=', e.response.data)
    } else {
      console.error('Error loading tasks (no response):', e?.message || e)
    }
  } finally {
    state.loading = false
  }
}

/** POST /createTask */
async function createTask() {
  if (!formCreate.name.trim()) return
  state.creating = true
  try {
    const payload: any = {
      name: formCreate.name.trim(),
      desc: formCreate.desc?.trim() || undefined,
      notes: formCreate.notes?.trim() || undefined,
    }
    if (formCreate.pid?.trim()) payload.pid = formCreate.pid.trim()
    if (formCreate.parentTaskId?.trim()) payload.parentTaskId = formCreate.parentTaskId.trim()

    const collabs = formCreate.collaboratorsCsv
      ?.split(',')
      .map(s => s.trim())
      .filter(Boolean)
    if (collabs?.length) payload.collaborators = collabs

    const sched: Schedule = {}
    if (formCreate.schedule.status) sched.status = formCreate.schedule.status
    if (formCreate.schedule.deadline) sched.deadline = formCreate.schedule.deadline
    if (formCreate.schedule.priority) sched.priority = formCreate.schedule.priority
    if (Object.keys(sched).length) payload.schedule = sched

    payload.userID = USER_ID
    await api.post('/createTask', payload)
    await loadTasks()
    ui.showCreate = false
    formCreate.name = ''
    formCreate.desc = ''
    formCreate.notes = ''
    formCreate.pid = ''
    formCreate.parentTaskId = ''
    formCreate.collaboratorsCsv = ''
    formCreate.schedule = { status: '', deadline: '', priority: '' }
  } catch (e) {
    console.error('Error creating task:', e)
  } finally {
    state.creating = false
  }
}

/** Open Edit */
async function openEdit(id: string) {
  state.editingId = id
  const taskFromList = state.tasks.find(x => x.id === id)
  if (taskFromList) {
    formEdit.name = taskFromList.name || ''
    formEdit.desc = taskFromList.desc || ''
    formEdit.notes = taskFromList.notes || ''
    formEdit.pid = taskFromList.pid || ''
    formEdit.parentTaskId = (taskFromList as any)?.parentTaskId || ''
    formEdit.collaboratorsCsv = (taskFromList.collaborators || []).join(',') || ''
    formEdit.schedule.status = ''
    formEdit.schedule.deadline = ''
  }
  ui.showEdit = true

  try {
    const { data } = await api.get(`/tasks/${id}`)
    let taskData: any = {}
    let scheduleData: any = {}
    if (data.task) {
      taskData = data.task
      scheduleData = data.schedule || {}
    } else if (data.id) {
      taskData = data
      scheduleData = data
    } else {
      taskData = data
    }

    if (taskData.name !== undefined) formEdit.name = taskData.name || ''
    if (taskData.desc !== undefined) formEdit.desc = taskData.desc || ''
    if (taskData.description !== undefined) formEdit.desc = taskData.description || ''
    if (taskData.notes !== undefined) formEdit.notes = taskData.notes || ''
    if (taskData.pid !== undefined) formEdit.pid = taskData.pid || ''
    if (taskData.parentTaskId !== undefined) formEdit.parentTaskId = taskData.parentTaskId || ''
    if (taskData.parent_task_id !== undefined) formEdit.parentTaskId = taskData.parent_task_id || ''

    if (taskData.collaborators !== undefined) {
      if (Array.isArray(taskData.collaborators)) {
        formEdit.collaboratorsCsv = taskData.collaborators.join(',')
      } else if (typeof taskData.collaborators === 'string') {
        formEdit.collaboratorsCsv = taskData.collaborators
      }
    }

    if (scheduleData.status !== undefined) formEdit.schedule.status = scheduleData.status || ''
    if (taskData.status !== undefined) formEdit.schedule.status = taskData.status || ''

    if (scheduleData.deadline !== undefined) {
      formEdit.schedule.deadline = scheduleData.deadline ? toLocalDatetimeInput(scheduleData.deadline) : ''
    } else if (taskData.deadline !== undefined) {
      formEdit.schedule.deadline = taskData.deadline ? toLocalDatetimeInput(taskData.deadline) : ''
    }
  } catch (e: any) {
    console.error('Error fetching detailed task data:', e?.response?.data || e?.message || e)
  }
}

/** PUT /{id} */
async function saveEdit() {
  if (!state.editingId) return
  state.saving = true
  try {
    const payload: Record<string, any> = {
      name: formEdit.name?.trim(),
      desc: formEdit.desc?.trim() || undefined,
      notes: formEdit.notes?.trim() || undefined,
      pid: formEdit.pid?.trim() || undefined,
      parentTaskId: formEdit.parentTaskId?.trim() || undefined,
    }

    const collabs = formEdit.collaboratorsCsv
      ?.split(',')
      .map(s => s.trim())
      .filter(Boolean)
    if (collabs?.length) payload.collaborators = collabs

    if (formEdit.schedule.status) payload.status = formEdit.schedule.status
    if (formEdit.schedule.deadline) payload.deadline = formEdit.schedule.deadline

    console.log('Requesting:', api.defaults.baseURL + '/' + state.editingId)
    
    await api.put(`/${state.editingId}`, payload)
    await loadTasks()
    ui.showEdit = false
  } catch (e) {
    console.error('Error saving task:', e)
  } finally {
    state.saving = false
  }
}

/** DELETE /{id} */
async function confirmDelete() {
  if (!state.editingId) return
  if (!confirm('Delete this task (and its schedules)?')) return
  try {
    await api.delete(`/${state.editingId}`)
    state.tasks = state.tasks.filter(t => t.id !== state.editingId)
    ui.showEdit = false
  } catch (e) {
    console.error('Error deleting task:', e)
  }
}

function toLocalDatetimeInput(iso: string) {
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  const yyyy = d.getFullYear()
  const mm = pad(d.getMonth() + 1)
  const dd = pad(d.getDate())
  const hh = pad(d.getHours())
  const mi = pad(d.getMinutes())
  return `${yyyy}-${mm}-${dd}T${hh}:${mi}`
}

onMounted(loadTasks)
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>