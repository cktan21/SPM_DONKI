<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// --- Shadcn-vue Component Imports ---
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from '@/components/ui/alert'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Stepper,
  StepperDescription,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from '@/components/ui/stepper'
import {
  ArrowLeft,
  Calendar,
  ChevronDown,
  FilePenLine,
  Flag,
  FolderOpen,
  Trash2,
  TriangleAlert,
  User,
  Clock,
  Circle,
  Tag,
  RefreshCw,
  Check,
  Loader,
  AlertTriangle as AlertTriangleIcon,
  Send,
  Paperclip,
  CheckCheck,
  Dot,
} from 'lucide-vue-next'

// --- Setup ---
const route = useRoute()
const router = useRouter()
const taskId = computed(() => route.params.id as string)

const task = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const expandedSubtasks = ref<Set<string>>(new Set())
const deleteDialogOpen = ref(false)
const itemToDelete = ref<{ id: string, type: 'task' | 'subtask' } | null>(null)
const messageInput = ref('')

// --- API bases ---
const API_BASE_URL = 'http://localhost:4000'
const TASKA_BASE_URL = 'http://localhost:5500'

// --- Mock data for changelog and chat (replace with real API calls later) ---
const mockChangelog = ref([
  {
    step: 1,
    title: 'Task created',
    description: 'Sarah Johnson created this task',
    timestamp: '2024-10-15T09:00:00',
    status: 'completed'
  },
  {
    step: 2,
    title: 'Status changed to Ongoing',
    description: 'Alex Chen updated the status',
    timestamp: '2024-10-18T14:30:00',
    status: 'completed'
  },
  {
    step: 3,
    title: 'Deadline extended',
    description: 'Maria Garcia extended the deadline to Nov 15',
    timestamp: '2024-10-20T10:15:00',
    status: 'active'
  },
])

const mockMessages = ref([
  { id: '1', sender: 'Alex Chen', message: 'Started working on the wireframes', timestamp: '10:30 AM', isOwn: false },
  { id: '2', sender: 'You', message: 'Great! Let me know if you need any feedback', timestamp: '10:32 AM', isOwn: true },
  { id: '3', sender: 'Maria Garcia', message: 'I can help with the chart components once wireframes are done', timestamp: '11:15 AM', isOwn: false },
  { id: '4', sender: 'You', message: 'Perfect timing! We should be ready by next week', timestamp: '11:20 AM', isOwn: true },
])

// ---------- Helpers ----------
const isUuid = (v: string) => typeof v === 'string' && v.trim().length === 36

const normalizeSchedule = (raw: any) => {
  if (!raw) return {}
  return raw?.data ?? raw
}

const normalizeTask = (x: any) => {
  if (!x) return null
  const schedule = normalizeSchedule(x?.schedule ?? {})
  const subtasks = Array.isArray(x?.subtasks) ? x.subtasks : []
  return {
    ...x,
    schedule,
    subtasks,
  }
}

const normalizeSubtask = (x: any) => {
  return {
    id: x?.id ?? '',
    name: x?.name ?? 'Untitled',
    desc: x?.desc ?? '',
    notes: x?.notes ?? '',
    priorityLevel: x?.priorityLevel ?? undefined,
    label: x?.label ?? '',
    status: x?.status ?? 'not started',
    deadline: x?.deadline ?? '',
    parentTaskId: x?.parentTaskId ?? null,
    pid: x?.pid ?? null,
    collaborators: Array.isArray(x?.collaborators) ? x.collaborators : [],
    created_by_uid: x?.created_by_uid ?? null,
    updated_timestamp: x?.updated_timestamp ?? null,
  }
}

// ---------- Fetchers ----------
const fetchMainTask = async (id: string) => {
  const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  })
  if (!res.ok) throw new Error(`Task fetch failed (${res.status})`)
  const text = await res.text()
  if (!text) throw new Error('Empty response from /tasks/{id} (composite)')

  const data = JSON.parse(text)
  const rawTask = data?.task ?? (data?.id ? data : null)
  return normalizeTask(rawTask)
}

const fetchSubtasks = async (id: string) => {
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
    const date = new Date(dateStr)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    return `${day}/${month}/${year}`
  } catch {
    return 'N/A'
  }
}

const formatDateShort = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } catch {
    return 'N/A'
  }
}

const formatTime = (dateStr: string | null | undefined) => {
  if (!dateStr) return ''
  try {
    return new Date(dateStr).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  } catch {
    return ''
  }
}

const capitalizeFirst = (str: string) => {
  if (!str) return 'Not Started'
  return str.charAt(0).toUpperCase() + str.slice(1)
}

const getStatusConfig = (status: string) => {
  const normalized = (status || '').toLowerCase()
  
  if (normalized === 'done' || normalized === 'completed') {
    return {
      label: 'Done',
      icon: Check,
      bgColor: 'bg-emerald-500/10',
      textColor: 'text-emerald-700',
      borderColor: 'border-emerald-200',
    }
  }
  
  if (normalized === 'ongoing') {
    return {
      label: 'Ongoing',
      icon: AlertTriangleIcon,
      bgColor: 'bg-blue-500/10',
      textColor: 'text-blue-700',
      borderColor: 'border-blue-200',
    }
  }
  
  return {
    label: 'To Do',
    icon: Loader,
    bgColor: 'bg-orange-500/10',
    textColor: 'text-orange-700',
    borderColor: 'border-orange-200',
  }
}

const getColorFromName = (name: string) => {
  const colors = [
    'bg-red-700', 'bg-blue-700', 'bg-green-700', 'bg-amber-700',
    'bg-purple-700', 'bg-pink-700', 'bg-indigo-700', 'bg-teal-700',
    'bg-orange-700', 'bg-cyan-700', 'bg-violet-700', 'bg-fuchsia-700'
  ]
  const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[hash % colors.length]
}

const toggleSubtask = (subtaskId: string) => {
  if (expandedSubtasks.value.has(subtaskId)) {
    expandedSubtasks.value.delete(subtaskId)
  } else {
    expandedSubtasks.value.add(subtaskId)
  }
}

const openDeleteDialog = (id: string, type: 'task' | 'subtask') => {
  itemToDelete.value = { id, type }
  deleteDialogOpen.value = true
}

const confirmDelete = async () => {
  if (!itemToDelete.value) return
  
  try {
    const response = await fetch(`${API_BASE_URL}/${itemToDelete.value.id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!response.ok) throw new Error('Failed to delete')
    
    if (itemToDelete.value.type === 'task') {
      router.push('/tasks')
    } else {
      await fetchTask()
    }
  } catch (err: any) {
    alert('Error deleting: ' + err.message)
  } finally {
    deleteDialogOpen.value = false
    itemToDelete.value = null
  }
}

const goToEditPage = (id: string) => {
  router.push(`/task/edit/${id}`)
}

const getInitials = (name: string | undefined) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const sendMessage = () => {
  if (!messageInput.value.trim()) return
  mockMessages.value.push({
    id: Date.now().toString(),
    sender: 'You',
    message: messageInput.value,
    timestamp: formatTime(new Date().toISOString()),
    isOwn: true
  })
  messageInput.value = ''
}

// --- User Data ---
const userData = useState<any>("userData")
const role = userData.value?.user?.role
const uid = userData.value?.user?.id

const canEditTask = computed(() => {
  if (!task.value) return false
  return role === 'manager' || uid === task.value.created_by_uid
})

const canEditSubtask = (subtask: any) => {
  return role === 'manager' || uid === subtask.created_by_uid
}

onMounted(async () => {
  await fetchTask()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
    <div class="container mx-auto max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <Button
          variant="ghost"
          size="sm"
          @click="router.back()"
          class="gap-2"
        >
          <ArrowLeft class="w-4 h-4" />
          <span class="hidden sm:inline">Back</span>
        </Button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-6">
        <Card>
          <CardHeader>
            <Skeleton class="h-10 w-3/4 mb-2" />
            <Skeleton class="h-4 w-1/2" />
          </CardHeader>
          <CardContent>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div class="lg:col-span-2">
                <Skeleton class="h-32 w-full" />
              </div>
              <div>
                <Skeleton class="h-64 w-full" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Error State -->
      <Alert v-else-if="error" variant="destructive">
        <TriangleAlert class="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{{ error }}</AlertDescription>
      </Alert>

      <!-- Main Content -->
      <div v-else-if="task" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Main Content (Desktop) / All Content (Mobile) -->
        <div class="lg:col-span-2 space-y-6 order-1 lg:order-1">
          <!-- Task Header Card -->
          <Card class="rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-4">
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-4">
                <div class="flex-1 space-y-3">
                  <CardTitle class="text-3xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
                    {{ task.name || 'Untitled Task' }}
                  </CardTitle>
                  <div class="flex flex-wrap items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
                    <div class="flex items-center gap-1.5">
                      <Clock class="w-3.5 h-3.5" />
                      <span>Updated {{ formatDateShort(task.updated_timestamp) }}</span>
                    </div>
                    <span class="text-slate-300 dark:text-slate-700">•</span>
                    <div v-if="task.created_by" class="flex items-center gap-1.5">
                      <User class="w-3.5 h-3.5" />
                      <span>Created by {{ task.created_by?.name }}</span>
                    </div>
                  </div>
                </div>
                <div v-if="canEditTask" class="flex gap-2 shrink-0">
                  <Button
                    @click="goToEditPage(task.id)"
                    size="sm"
                    variant="outline"
                    class="gap-2"
                  >
                    <FilePenLine class="w-4 h-4" />
                    <span class="hidden sm:inline">Edit</span>
                  </Button>
                  <Button
                    @click="openDeleteDialog(task.id, 'task')"
                    size="sm"
                    variant="outline"
                    class="gap-2 text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200 dark:border-red-800 dark:hover:bg-red-950"
                  >
                    <Trash2 class="w-4 h-4" />
                    <span class="hidden sm:inline">Delete</span>
                  </Button>
                </div>
              </div>

              <!-- Status Badge -->
              <Badge
                :class="`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border font-medium text-sm w-fit ${getStatusConfig(task.schedule?.status).bgColor} ${getStatusConfig(task.schedule?.status).textColor} ${getStatusConfig(task.schedule?.status).borderColor}`"
              >
                <component :is="getStatusConfig(task.schedule?.status).icon" class="h-3.5 w-3.5" />
                {{ getStatusConfig(task.schedule?.status).label }}
              </Badge>
            </CardHeader>

            <CardContent class="p-6 pt-0 space-y-6">
              <!-- Description -->
              <div class="space-y-2">
                <Label class="text-sm font-semibold text-slate-900 dark:text-slate-100">Description</Label>
                <div class="p-4 rounded-lg border border-slate-200 bg-slate-50/50 dark:border-slate-800 dark:bg-slate-800/50">
                  <p class="text-sm text-slate-700 leading-relaxed dark:text-slate-300 whitespace-pre-wrap">
                    {{ task.desc || 'No description provided.' }}
                  </p>
                </div>
              </div>

              <!-- Notes -->
              <div class="space-y-2">
                <Label class="text-sm font-semibold text-slate-900 dark:text-slate-100">Notes</Label>
                <div class="p-4 rounded-lg border border-slate-200 bg-slate-50/50 dark:border-slate-800 dark:bg-slate-800/50">
                  <p class="text-sm text-slate-700 leading-relaxed dark:text-slate-300 whitespace-pre-wrap">
                    {{ task.notes || 'No notes provided.' }}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Task Details Card (Mobile Only) -->
          <Card class="lg:hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-3">
              <CardTitle class="text-lg">Task Details</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-3 space-y-5">
              <!-- Deadline -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Calendar class="w-3.5 h-3.5" />
                  Deadline
                </div>
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {{ formatDate(task.schedule?.deadline) }}
                </p>
              </div>

              <Separator />

              <!-- Priority -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Flag class="w-3.5 h-3.5" />
                  Priority Level
                </div>
                <div v-if="task.priorityLevel !== undefined && task.priorityLevel !== null" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-orange-500/10 text-orange-700 border border-orange-200 text-sm font-medium dark:bg-orange-500/20 dark:text-orange-400">
                  <Flag class="w-3.5 h-3.5" />
                  P{{ task.priorityLevel }}
                </div>
                <p v-else class="text-sm font-medium text-slate-900 dark:text-slate-100">N/A</p>
              </div>

              <Separator v-if="task.label" />

              <!-- Label -->
              <div v-if="task.label" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Tag class="w-3.5 h-3.5" />
                  Label
                </div>
                <Badge variant="outline" class="capitalize text-xs px-2.5 py-1 bg-purple-500/10 text-purple-700 border-purple-200 dark:bg-purple-500/20 dark:text-purple-400">
                  {{ task.label }}
                </Badge>
              </div>

              <Separator v-if="task.schedule?.is_recurring" />

              <!-- Recurring -->
              <div v-if="task.schedule?.is_recurring" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <RefreshCw class="w-3.5 h-3.5" />
                  Recurring
                </div>
                <div class="space-y-1">
                  <Badge variant="outline" class="text-xs">
                    {{ task.schedule.frequency || 'Custom' }}
                  </Badge>
                  <p v-if="task.schedule.next_occurrence" class="text-xs text-slate-600 dark:text-slate-400">
                    Next: {{ formatDate(task.schedule.next_occurrence) }}
                  </p>
                </div>
              </div>

              <Separator />

              <!-- Project -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <FolderOpen class="w-3.5 h-3.5" />
                  Project
                </div>
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {{ task.project?.name || 'No Project' }}
                </p>
              </div>

              <Separator v-if="task.parent_task" />

              <!-- Parent Task -->
              <div v-if="task.parent_task" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <FolderOpen class="w-3.5 h-3.5" />
                  Parent Task
                </div>
                <button
                  @click="router.push(`/task/${task.parent_task.id}`)"
                  class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 hover:underline text-left"
                >
                  {{ task.parent_task.name || 'View Parent Task' }}
                </button>
              </div>

              <Separator />

              <!-- Collaborators -->
              <div class="space-y-3">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <User class="w-3.5 h-3.5" />
                  Collaborators
                </div>
                <div v-if="task.collaborators?.length" class="space-y-2">
                  <div
                    v-for="(collab, idx) in task.collaborators"
                    :key="idx"
                    class="flex items-center gap-2.5 p-2 rounded-lg border border-slate-200 bg-slate-50/50 hover:bg-slate-100/50 transition-colors dark:border-slate-800 dark:bg-slate-800/50 dark:hover:bg-slate-800"
                  >
                    <Avatar class="h-8 w-8">
                      <AvatarFallback :class="`text-white text-xs font-semibold ${getColorFromName(collab?.name || collab)}`">
                        {{ getInitials(collab?.name || collab) }}
                      </AvatarFallback>
                    </Avatar>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-slate-900 truncate dark:text-slate-100">
                        {{ typeof collab === 'string' ? collab : (collab?.name || 'Unknown') }}
                      </p>
                      <p v-if="typeof collab !== 'string' && collab?.email" class="text-xs text-slate-500 truncate dark:text-slate-500">
                        {{ collab.email }}
                      </p>
                    </div>
                  </div>
                </div>
                <p v-else class="text-sm text-slate-600 dark:text-slate-400">None</p>
              </div>
            </CardContent>
          </Card>

          <!-- Subtasks Section -->
          <Card class="rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-4">
              <div class="flex items-center justify-between">
                <div>
                  <CardTitle class="text-lg font-semibold text-slate-900 dark:text-slate-100">Subtasks</CardTitle>
                  <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
                    {{ task.subtasks?.length || 0 }} subtask{{ task.subtasks?.length !== 1 ? 's' : '' }}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent class="px-6 pb-6 pt-0">
              <div v-if="task.subtasks && task.subtasks.length > 0" class="space-y-2">
                <Collapsible
                  v-for="sub in task.subtasks"
                  :key="sub.id"
                  class="group border border-slate-200 rounded-lg hover:shadow-md transition-all dark:border-slate-800"
                  :open="expandedSubtasks.has(sub.id)"
                  @update:open="() => toggleSubtask(sub.id)"
                >
                  <div class="flex items-start gap-3 p-3">
                    <CollapsibleTrigger as-child>
                      <Button variant="ghost" size="sm" class="h-8 w-8 p-0 shrink-0 mt-0.5 hover:bg-slate-100 dark:hover:bg-slate-800">
                        <ChevronDown 
                          class="h-4 w-4 transition-transform duration-200" 
                          :class="{ '-rotate-90': !expandedSubtasks.has(sub.id) }" 
                        />
                      </Button>
                    </CollapsibleTrigger>
                    
                    <div class="flex-1 min-w-0 space-y-2">
                      <div class="flex items-start justify-between gap-3">
                        <button 
                          @click="router.push(`/task/${sub.id}`)"
                          class="font-semibold text-sm leading-tight text-slate-900 dark:text-slate-100 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-left"
                        >
                          {{ sub.name }}
                        </button>
                        <Badge
                          :class="`inline-flex items-center gap-1 px-2.5 py-1 rounded-md border text-xs font-medium shrink-0 ${getStatusConfig(sub.status).bgColor} ${getStatusConfig(sub.status).textColor} ${getStatusConfig(sub.status).borderColor}`"
                        >
                          <component :is="getStatusConfig(sub.status).icon" class="h-3 w-3" />
                          {{ getStatusConfig(sub.status).label }}
                        </Badge>
                      </div>
                      
                      <div class="flex flex-wrap items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
                        <div class="flex items-center gap-1">
                          <Calendar class="w-3 h-3" />
                          <span>{{ formatDate(sub.deadline) }}</span>
                        </div>
                        <div v-if="sub.priorityLevel !== undefined && sub.priorityLevel !== null" class="flex items-center gap-1">
                          <Flag class="w-3 h-3" />
                          <span>P{{ sub.priorityLevel }}</span>
                        </div>
                        <div v-if="sub.label" class="px-2 py-0.5 bg-slate-100 text-slate-700 rounded-md dark:bg-slate-800 dark:text-slate-300">
                          {{ sub.label }}
                        </div>
                      </div>
                    </div>

                    <div v-if="canEditSubtask(sub)" class="flex gap-1 shrink-0">
                      <Button 
                        @click.stop="goToEditPage(sub.id)" 
                        size="icon" 
                        variant="ghost" 
                        class="h-8 w-8 hover:bg-slate-100 dark:hover:bg-slate-800"
                      >
                        <FilePenLine class="w-4 h-4 text-slate-600 dark:text-slate-400" />
                      </Button>
                      <Button 
                        @click.stop="openDeleteDialog(sub.id, 'subtask')" 
                        size="icon" 
                        variant="ghost" 
                        class="h-8 w-8 hover:bg-red-50 dark:hover:bg-red-900/20"
                      >
                        <Trash2 class="w-4 h-4 text-red-600" />
                      </Button>
                    </div>
                  </div>

                  <CollapsibleContent>
                    <div class="px-3 pb-3 pt-2 border-t border-slate-200 bg-slate-50/50 dark:border-slate-800 dark:bg-slate-800/50">
                      <div class="pl-11 space-y-2">
                        <div v-if="sub.desc" class="space-y-1">
                          <Label class="text-xs font-semibold text-slate-900 dark:text-slate-100">Description</Label>
                          <p class="text-sm text-slate-600 leading-relaxed dark:text-slate-400">{{ sub.desc }}</p>
                        </div>
                        <div v-if="sub.notes" class="space-y-1">
                          <Label class="text-xs font-semibold text-slate-900 dark:text-slate-100">Notes</Label>
                          <p class="text-sm text-slate-600 leading-relaxed dark:text-slate-400">{{ sub.notes }}</p>
                        </div>
                      </div>
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              </div>
              
              <div v-else class="flex flex-col items-center justify-center py-12 text-center border border-dashed rounded-lg border-slate-200 dark:border-slate-800">
                <div class="rounded-full bg-slate-100 p-3 mb-3 dark:bg-slate-800">
                  <Circle class="w-6 h-6 text-slate-400 dark:text-slate-600" />
                </div>
                <p class="text-sm font-medium text-slate-600 dark:text-slate-400">No subtasks yet</p>
                <p class="text-xs text-slate-500 mt-1 dark:text-slate-500">Subtasks will appear here when created</p>
              </div>
            </CardContent>
          </Card>

          <!-- Chat Section -->
          <Card class="rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-4">
              <CardTitle class="text-lg font-semibold text-slate-900 dark:text-slate-100">Chat</CardTitle>
              <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
                Discuss this task with your team
              </CardDescription>
            </CardHeader>
            <CardContent class="p-6 pt-0 space-y-4">
              <!-- Messages -->
              <div class="space-y-3 max-h-96 overflow-y-auto pr-2">
                <div
                  v-for="msg in mockMessages"
                  :key="msg.id"
                  :class="`flex ${msg.isOwn ? 'justify-end' : 'justify-start'}`"
                >
                  <div :class="`max-w-[70%] ${msg.isOwn ? 'order-2' : 'order-1'}`">
                    <p v-if="!msg.isOwn" class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-1 px-1">
                      {{ msg.sender }}
                    </p>
                    <div :class="`rounded-2xl px-4 py-2.5 ${
                      msg.isOwn 
                        ? 'bg-blue-600 text-white rounded-br-sm' 
                        : 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 rounded-bl-sm'
                    }`">
                      <p class="text-sm">{{ msg.message }}</p>
                      <div class="flex items-center gap-1 justify-end mt-1">
                        <span :class="`text-xs ${msg.isOwn ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'}`">
                          {{ msg.timestamp }}
                        </span>
                        <CheckCheck v-if="msg.isOwn" class="w-3 h-3 text-blue-100" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Message Input -->
              <div class="flex items-center gap-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                <Button variant="ghost" size="icon" class="h-9 w-9 text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800">
                  <Paperclip class="w-5 h-5" />
                </Button>
                <Input
                  v-model="messageInput"
                  type="text"
                  placeholder="Type a message..."
                  @keyup.enter="sendMessage"
                  class="flex-1 text-sm border-slate-200 dark:border-slate-700 dark:bg-slate-800"
                />
                <Button @click="sendMessage" size="icon" class="h-9 w-9 bg-blue-600 hover:bg-blue-700 text-white">
                  <Send class="w-5 h-5" />
                </Button>
              </div>
            </CardContent>
          </Card>

          <!-- Change Log Section -->
          <Card class="rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-4">
              <CardTitle class="text-lg font-semibold text-slate-900 dark:text-slate-100">Change Log</CardTitle>
              <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
                Track all changes made to this task
              </CardDescription>
            </CardHeader>
            <CardContent class="p-6 pt-0">
              <Stepper orientation="vertical" class="flex flex-col justify-start gap-6">
                <StepperItem
                  v-for="change in mockChangelog"
                  :key="change.step"
                  v-slot="{ state }"
                  class="relative flex items-start gap-4"
                  :step="change.step"
                >
                  <StepperSeparator
                    v-if="change.step !== mockChangelog[mockChangelog.length - 1]?.step"
                    class="absolute left-[18px] top-[38px] block h-[calc(100%+0.5rem)] w-0.5 shrink-0 rounded-full bg-slate-200 dark:bg-slate-800 group-data-[state=completed]:bg-blue-500"
                  />
                  <StepperTrigger as-child>
                    <Button
                      :variant="state === 'completed' || state === 'active' ? 'default' : 'outline'"
                      size="icon"
                      class="z-10 rounded-full shrink-0 h-9 w-9"
                      :class="[state === 'active' && 'ring-2 ring-blue-500 ring-offset-2 ring-offset-background']"
                    >
                      <Check v-if="state === 'completed'" class="h-4 w-4" />
                      <Circle v-if="state === 'active'" class="h-4 w-4" />
                      <Dot v-if="state === 'inactive'" class="h-5 w-5" />
                    </Button>
                  </StepperTrigger>
                  <div class="flex flex-col gap-1 pb-4">
                    <StepperTitle
                      :class="[state === 'active' && 'text-blue-600 dark:text-blue-400']"
                      class="text-sm font-semibold transition text-slate-900 dark:text-slate-100"
                    >
                      {{ change.title }}
                    </StepperTitle>
                    <StepperDescription
                      :class="[state === 'active' && 'text-blue-600 dark:text-blue-400']"
                      class="text-xs text-slate-600 transition dark:text-slate-400"
                    >
                      {{ change.description }}
                    </StepperDescription>
                    <p class="text-xs text-slate-500 mt-1 dark:text-slate-500">
                      {{ formatDateShort(change.timestamp) }} at {{ formatTime(change.timestamp) }}
                    </p>
                  </div>
                </StepperItem>
              </Stepper>
            </CardContent>
          </Card>
        </div>

        <!-- Right Column: Details Sidebar (Desktop Only) -->
        <div class="lg:col-span-1 hidden lg:block order-2">
          <Card class="rounded-xl border border-slate-200 bg-white shadow-sm sticky top-6 dark:border-slate-800 dark:bg-slate-900/50">
            <CardHeader class="p-6 pb-3">
              <CardTitle class="text-lg">Task Details</CardTitle>
            </CardHeader>
            <CardContent class="p-6 pt-3 space-y-5">
              <!-- Deadline -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Calendar class="w-3.5 h-3.5" />
                  Deadline
                </div>
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {{ formatDate(task.schedule?.deadline) }}
                </p>
              </div>

              <Separator />

              <!-- Priority -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Flag class="w-3.5 h-3.5" />
                  Priority Level
                </div>
                <div v-if="task.priorityLevel !== undefined && task.priorityLevel !== null" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-orange-500/10 text-orange-700 border border-orange-200 text-sm font-medium dark:bg-orange-500/20 dark:text-orange-400">
                  <Flag class="w-3.5 h-3.5" />
                  P{{ task.priorityLevel }}
                </div>
                <p v-else class="text-sm font-medium text-slate-900 dark:text-slate-100">N/A</p>
              </div>

              <Separator v-if="task.label" />

              <!-- Label -->
              <div v-if="task.label" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <Tag class="w-3.5 h-3.5" />
                  Label
                </div>
                <Badge variant="outline" class="capitalize text-xs px-2.5 py-1 bg-purple-500/10 text-purple-700 border-purple-200 dark:bg-purple-500/20 dark:text-purple-400">
                  {{ task.label }}
                </Badge>
              </div>

              <Separator v-if="task.schedule?.is_recurring" />

              <!-- Recurring -->
              <div v-if="task.schedule?.is_recurring" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <RefreshCw class="w-3.5 h-3.5" />
                  Recurring
                </div>
                <div class="space-y-1">
                  <Badge variant="outline" class="text-xs">
                    {{ task.schedule.frequency || 'Custom' }}
                  </Badge>
                  <p v-if="task.schedule.next_occurrence" class="text-xs text-slate-600 dark:text-slate-400">
                    Next: {{ formatDate(task.schedule.next_occurrence) }}
                  </p>
                </div>
              </div>

              <Separator />

              <!-- Project -->
              <div class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <FolderOpen class="w-3.5 h-3.5" />
                  Project
                </div>
                <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
                  {{ task.project?.name || 'No Project' }}
                </p>
              </div>

              <Separator v-if="task.parent_task" />

              <!-- Parent Task -->
              <div v-if="task.parent_task" class="space-y-2">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <FolderOpen class="w-3.5 h-3.5" />
                  Parent Task
                </div>
                <button
                  @click="router.push(`/task/${task.parent_task.id}`)"
                  class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 hover:underline text-left"
                >
                  {{ task.parent_task.name || 'View Parent Task' }}
                </button>
              </div>

              <Separator />

              <!-- Collaborators -->
              <div class="space-y-3">
                <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-600 dark:text-slate-400">
                  <User class="w-3.5 h-3.5" />
                  Collaborators
                </div>
                <div v-if="task.collaborators?.length" class="space-y-2">
                  <div
                    v-for="(collab, idx) in task.collaborators"
                    :key="idx"
                    class="flex items-center gap-2.5 p-2 rounded-lg border border-slate-200 bg-slate-50/50 hover:bg-slate-100/50 transition-colors dark:border-slate-800 dark:bg-slate-800/50 dark:hover:bg-slate-800"
                  >
                    <Avatar class="h-8 w-8">
                      <AvatarFallback :class="`text-white text-xs font-semibold ${getColorFromName(collab?.name || collab)}`">
                        {{ getInitials(collab?.name || collab) }}
                      </AvatarFallback>
                    </Avatar>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-slate-900 truncate dark:text-slate-100">
                        {{ typeof collab === 'string' ? collab : (collab?.name || 'Unknown') }}
                      </p>
                      <p v-if="typeof collab !== 'string' && collab?.email" class="text-xs text-slate-500 truncate dark:text-slate-500">
                        {{ collab.email }}
                      </p>
                    </div>
                  </div>
                </div>
                <p v-else class="text-sm text-slate-600 dark:text-slate-400">None</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      
      <!-- No Data State -->
      <div v-else class="flex items-center justify-center py-20">
        <Card class="w-full max-w-md rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900/50">
          <CardContent class="pt-6 text-center">
            <TriangleAlert class="w-12 h-12 text-slate-400 mx-auto mb-3 dark:text-slate-600" />
            <p class="text-lg font-semibold text-slate-900 dark:text-slate-100">No task data found</p>
            <p class="text-sm text-slate-600 mt-1 dark:text-slate-400">The task you're looking for doesn't exist</p>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <AlertDialog v-model:open="deleteDialogOpen">
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the {{ itemToDelete?.type === 'task' ? 'task and all its subtasks' : 'subtask' }}.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction @click="confirmDelete" class="bg-destructive hover:bg-destructive/90">
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  </div>
</template>