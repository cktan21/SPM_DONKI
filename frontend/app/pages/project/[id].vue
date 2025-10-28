<script setup lang="ts">
import { onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { columns } from './components/columns'
import DataTable from './components/DataTable.vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

// Task and Project interfaces
interface Collaborator {
  id: string
  name: string
}

interface Task {
  id: string
  name: string
  created_by_uid: string
  updated_timestamp: string
  parentTaskId: string | null
  collaborators: Collaborator[] | null
  pid: string
  desc: string
  notes: string
  priorityLevel: number
  priorityLabel: string
  label?: string | null
  status?: string | null
  deadline?: string | null
  is_recurring?: boolean | null
  next_occurrence?: string | null
  start?: string | null
  sid?: string | null
}

interface Project {
  id: string
  uid: string
  name: string
  desc?: string | null
  created_at: string
  tasks: Task[]
}

// Router
const router = useRouter()
const route = useRoute()

// Fetch selected project from global state
const selectedProject = useState<Project | null>('selectedProject')
const loading = ref(false)
const error = ref<string | null>(null)

// Get current user data from auth state
const userData = useState<{ user: { id: string; email: string; role: string; name: string } } | null>("userData")

// Fetch project by project ID
const fetchProjectById = async (projectId: string) => {
  loading.value = true
  error.value = null
  
  try {
    const res = await fetch(`http://127.0.0.1:4100/pid/${projectId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (!res.ok) throw new Error(`Failed to fetch project: ${res.status}`)
    
    const data = await res.json()
    selectedProject.value = data.project
    console.log('Fetched project by ID:', data.project)
  } catch (err: any) {
    console.error('Error fetching project:', err)
    error.value = err.message || 'Failed to fetch project'
  } finally {
    loading.value = false
  }
}

// On mount, check if project is in state, otherwise fetch from URL
onMounted(async () => {
  const projectId = route.params.id as string
  
  if (!selectedProject.value && projectId) {
    // No project in state but we have ID in URL - fetch it
    await fetchProjectById(projectId)
  } else if (selectedProject.value && projectId !== selectedProject.value.id) {
    // URL ID doesn't match state - fetch from URL
    await fetchProjectById(projectId)
  } else if (selectedProject.value) {
    console.log('Using project from state:', selectedProject.value)
  } else {
    console.warn('No project ID in URL and no project in state')
  }
})

// Watch for route changes
watch(() => route.params.id, async (newId) => {
  if (newId && typeof newId === 'string') {
    await fetchProjectById(newId)
  }
})

// Filtered main + sub tasks for current user (role-based)
const mainTasks = computed(() => {
  if (!selectedProject.value?.tasks || !userData.value?.user?.id) return []

  const currentUserId = userData.value.user.id
  const userRole = userData.value.user.role?.toLowerCase() || 'staff'
  const allTasks = selectedProject.value.tasks

  // Admin, Manager, and HR can see ALL tasks
  const hasFullAccess = ['admin', 'manager', 'hr'].includes(userRole)

  // Step 1️⃣: Get only the main tasks that the user can access
  const visibleMainTasks = allTasks.filter(task => {
    if (task.parentTaskId) return false // only main tasks

    // Full access roles see everything
    if (hasFullAccess) return true

    // Staff only see tasks they created or collaborate on
    const isCreator = task.created_by_uid === currentUserId
    const collaborators = Array.isArray(task.collaborators) ? task.collaborators : []
    const isCollaborator = collaborators.some(
      c => c?.id?.toString() === currentUserId.toString()
    )

    return isCreator || isCollaborator
  })

  // Step 2️⃣: For each visible main task, attach its subtasks
  const visibleTasksWithSubtasks = visibleMainTasks.map(mainTask => {
    const subtasks = allTasks.filter(t => t.parentTaskId === mainTask.id)
    return { ...mainTask, subtasks }
  })

  return visibleTasksWithSubtasks
})

const subtasksByParentId = computed(() => {
  if (!selectedProject.value?.tasks || !userData.value?.user?.id) return {}
  
  const currentUserId = userData.value.user.id
  const map: Record<string, Task[]> = {}
  
  // Get list of accessible parent task IDs
  const accessibleParentIds = new Set(mainTasks.value.map(t => t.id))
  
  selectedProject.value.tasks.forEach(task => {
    const parentId = task.parentTaskId
    // Only include subtasks whose parent is accessible
    if (parentId && accessibleParentIds.has(parentId)) {
      if (!map[parentId]) {
        map[parentId] = []
      }
      map[parentId].push(task)
    }
  })
  return map
})

// Transform main tasks for the table (excluding subtasks)
const transformedTasks = computed(() => {
  return mainTasks.value.map(task => ({
    // Keep all original fields
    id: task.id,
    name: task.name,
    desc: task.desc,
    notes: task.notes,
    priorityLevel: task.priorityLevel,
    priorityLabel: task.priorityLabel,
    created_by_uid: task.created_by_uid,
    updated_timestamp: task.updated_timestamp,
    parentTaskId: task.parentTaskId,
    collaborators: task.collaborators,
    pid: task.pid,
    
    // Map to table column fields
    title: task.name,
    priority: task.priorityLevel,
    status: task.status || null,
    deadline: task.deadline || null,
    label: task.label || null,
    
    // Add subtasks for this task
    subtasks: subtasksByParentId.value[task.id]?.map(sub => ({
      id: sub.id,
      title: sub.name,
      status: sub.status || null,
      deadline: sub.deadline || null,
      label: sub.label || null,
      priority: sub.priorityLevel
    })) || []
  }))
})

// Calculate progress data from MAIN TASKS + SUBTASKS
const progressData = computed(() => {
  if (!selectedProject.value?.tasks) {
    return { done: 0, ongoing: 0, toDo: 0, total: 0 }
  }

  // Get all accessible tasks (main tasks + their subtasks)
  const allAccessibleTasks: Task[] = []
  
  mainTasks.value.forEach(mainTask => {
    allAccessibleTasks.push(mainTask)
    const subtasks = subtasksByParentId.value[mainTask.id] || []
    allAccessibleTasks.push(...subtasks)
  })

  const done = allAccessibleTasks.filter(t => t.status === 'done').length
  const ongoing = allAccessibleTasks.filter(t => t.status === 'ongoing').length
  const toDo = allAccessibleTasks.filter(t => t.status === 'to do').length
  const total = allAccessibleTasks.length

  return { done, ongoing, toDo, total }
})

// Calculate donut chart segments
const chartSegments = computed(() => {
  const { done, ongoing, toDo, total } = progressData.value
  if (total === 0) return { donePercent: 0, ongoingPercent: 0, toDoPercent: 0 }

  return {
    donePercent: (done / total) * 100,
    ongoingPercent: (ongoing / total) * 100,
    toDoPercent: (toDo / total) * 100,
  }
})

// Get unique collaborators from accessible tasks only (including subtasks) + current user
const uniqueCollaborators = computed(() => {
  if (!selectedProject.value?.tasks || !userData.value?.user?.id) return []

  const collabMap = new Map<string, { id: string; name: string }>()
  const currentUserId = userData.value.user.id
  const currentUserName = userData.value.user.name
  const accessibleParentIds = new Set(mainTasks.value.map(t => t.id))
  
  // Add current user first
  collabMap.set(currentUserId, { id: currentUserId, name: currentUserName })
  
  // Iterate through all tasks
  selectedProject.value.tasks.forEach(task => {
    // Include task if it's a main task the user has access to, or a subtask of an accessible parent
    const isAccessibleMainTask = !task.parentTaskId && (
      task.created_by_uid === currentUserId || 
      task.collaborators?.some(c => c && c.id === currentUserId)
    )
    const isAccessibleSubtask = task.parentTaskId && accessibleParentIds.has(task.parentTaskId)
    
    if (isAccessibleMainTask || isAccessibleSubtask) {
      if (task.collaborators && Array.isArray(task.collaborators)) {
        task.collaborators.forEach(collab => {
          if (collab && typeof collab === 'object' && 'id' in collab && 'name' in collab) {
            const collaborator = collab as { id: string; name: string }
            collabMap.set(collaborator.id, { id: collaborator.id, name: collaborator.name })
          }
        })
      }
    }
  })

  return Array.from(collabMap.values()).map((collab, index) => ({
    id: collab.id,
    name: collab.name,
    initials: getInitialsFromName(collab.name),
    color: getColorForIndex(index),
    isCurrentUser: collab.id === currentUserId
  }))
})

// Helper function to generate initials from name
const getInitialsFromName = (name: string): string => {
  if (!name) return 'NA'
  const words = name.trim().split(/\s+/).filter(w => w.length > 0)
  if (words.length === 0) return 'NA'
  if (words.length === 1) {
    return (words[0]?.slice(0, 2) || 'NA').toUpperCase()
  }
  return ((words[0]?.[0] || '') + (words[words.length - 1]?.[0] || '')).toUpperCase() || 'NA'
}

// Helper function to get color based on index
const getColorForIndex = (index: number): string => {
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-purple-500',
    'bg-orange-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-red-500',
    'bg-yellow-500',
    'bg-teal-500',
    'bg-cyan-500'
  ]
  return colors[index % colors.length] || 'bg-blue-500'
}

// SVG path calculation for donut chart
const getCircleProps = (percent: number, offset: number) => {
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const length = (percent / 100) * circumference
  
  return {
    radius,
    circumference,
    length,
    offset: -offset
  }
}

const projectTitle = computed(() =>
  selectedProject.value
    ? `${selectedProject.value.name}'s Project Dashboard`
    : 'Project Dashboard'
)

const projectDescription = computed(() =>
  selectedProject.value
    ? `${selectedProject.value.desc}`
    : 'This is a wonderful description for the project'
)

const handleCreateTask = () => {
  const projectId = route.params.id as string
  router.push(`./createTask/${projectId}`)
}
</script>

<template>
  <div class="container mx-auto py-10 px-3">
    <div class="space-y-6">
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div class="w-full sm:w-auto">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ projectTitle }}
          </h1>
          <p class="text-muted-foreground w-full sm:w-auto">
            {{ projectDescription }}
          </p>
        </div>
        <!-- Desktop Create Button - Hidden, will be shown below with "Tasks" -->
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8 text-muted-foreground">
        Loading project...
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8 text-destructive">
        {{ error }}
      </div>

      <!-- Progress and Collaborators Cards - RESPONSIVE -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Progress Card -->
        <Card>
          <CardHeader>
            <CardTitle class="text-lg sm:text-xl">Progress</CardTitle>
          </CardHeader>
          <CardContent class="flex flex-col items-center px-4 sm:px-6">
            <!-- Donut Chart - Smaller on mobile -->
            <div class="relative w-36 h-36 sm:w-48 sm:h-48 mb-4 sm:mb-6">
              <svg class="transform -rotate-90 w-full h-full" viewBox="0 0 192 192">
                <!-- Background circle -->
                <circle
                  cx="96"
                  cy="96"
                  :r="getCircleProps(0, 0).radius"
                  class="fill-none stroke-gray-200"
                  stroke-width="28"
                />
                
                <!-- Done segment (green) -->
                <circle
                  v-if="progressData.done > 0"
                  cx="96"
                  cy="96"
                  :r="getCircleProps(chartSegments.donePercent, 0).radius"
                  class="fill-none stroke-green-500 transition-all duration-500"
                  stroke-width="28"
                  :stroke-dasharray="`${getCircleProps(chartSegments.donePercent, 0).length} ${getCircleProps(chartSegments.donePercent, 0).circumference - getCircleProps(chartSegments.donePercent, 0).length}`"
                  stroke-dashoffset="0"
                  stroke-linecap="round"
                />
                
                <!-- Ongoing segment (blue) -->
                <circle
                  v-if="progressData.ongoing > 0"
                  cx="96"
                  cy="96"
                  :r="getCircleProps(chartSegments.ongoingPercent, getCircleProps(chartSegments.donePercent, 0).length).radius"
                  class="fill-none stroke-blue-500 transition-all duration-500"
                  stroke-width="28"
                  :stroke-dasharray="`${getCircleProps(chartSegments.ongoingPercent, 0).length} ${getCircleProps(chartSegments.ongoingPercent, 0).circumference - getCircleProps(chartSegments.ongoingPercent, 0).length}`"
                  :stroke-dashoffset="getCircleProps(chartSegments.ongoingPercent, getCircleProps(chartSegments.donePercent, 0).length).offset"
                  stroke-linecap="round"
                />
                
                <!-- To Do segment (orange) -->
                <circle
                  v-if="progressData.toDo > 0"
                  cx="96"
                  cy="96"
                  :r="getCircleProps(chartSegments.toDoPercent, getCircleProps(chartSegments.donePercent, 0).length + getCircleProps(chartSegments.ongoingPercent, 0).length).radius"
                  class="fill-none stroke-orange-500 transition-all duration-500"
                  stroke-width="28"
                  :stroke-dasharray="`${getCircleProps(chartSegments.toDoPercent, 0).length} ${getCircleProps(chartSegments.toDoPercent, 0).circumference - getCircleProps(chartSegments.toDoPercent, 0).length}`"
                  :stroke-dashoffset="-(getCircleProps(chartSegments.donePercent, 0).length + getCircleProps(chartSegments.ongoingPercent, 0).length)"
                  stroke-linecap="round"
                />
              </svg>
              
              <!-- Center text - Changed to "Total Tasks" -->
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-2xl sm:text-3xl font-bold">{{ progressData.total }}</div>
                  <div class="text-xs sm:text-sm text-muted-foreground">Total Tasks</div>
                </div>
              </div>
            </div>

            <!-- Legend - No more fractions, just numbers -->
            <div class="w-full space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-green-500 shrink-0"></div>
                  <span class="text-xs sm:text-sm">Done</span>
                </div>
                <span class="text-xs sm:text-sm font-medium">{{ progressData.done }}</span>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-blue-500 shrink-0"></div>
                  <span class="text-xs sm:text-sm">Ongoing</span>
                </div>
                <span class="text-xs sm:text-sm font-medium">{{ progressData.ongoing }}</span>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-orange-500 shrink-0"></div>
                  <span class="text-xs sm:text-sm">To Do</span>
                </div>
                <span class="text-xs sm:text-sm font-medium">{{ progressData.toDo }}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Collaborators Card -->
        <Card>
          <CardHeader>
            <CardTitle class="text-lg sm:text-xl">Collaborators</CardTitle>
          </CardHeader>
          <CardContent class="px-4 sm:px-6">
            <div v-if="uniqueCollaborators.length > 0" class="space-y-4 sm:space-y-6">
              <!-- Avatar Group - Overlapping Style -->
              <div>
                <p class="text-xs sm:text-sm text-muted-foreground mb-3">Team Members</p>
                <div class="flex items-center -space-x-2">
                  <div
                    v-for="collab in uniqueCollaborators.slice(0, 5)"
                    :key="collab.id"
                    :class="`w-8 h-8 sm:w-10 sm:h-10 rounded-full ${collab.color} flex items-center justify-center text-white text-xs sm:text-sm font-medium border-2 ${collab.isCurrentUser ? 'border-amber-200' : 'border-white'} hover:z-10 transition-transform hover:scale-110 cursor-pointer`"
                    :title="collab.isCurrentUser ? `${collab.name} (You)` : collab.name"
                  >
                    {{ collab.initials }}
                  </div>
                  <div
                    v-if="uniqueCollaborators.length > 5"
                    class="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gray-300 flex items-center justify-center text-gray-700 text-xs sm:text-sm font-medium border-2 border-white"
                  >
                    +{{ uniqueCollaborators.length - 5 }}
                  </div>
                </div>
              </div>

              <!-- Badge/Chip Style - All Members with FULL WIDTH WRAP -->
              <div>
                <p class="text-xs sm:text-sm text-muted-foreground mb-3">All Members ({{ uniqueCollaborators.length }})</p>
                <div class="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                  <div
                    v-for="collab in uniqueCollaborators"
                    :key="collab.id"
                    :class="`inline-flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full ${collab.isCurrentUser ? 'bg-amber-50' : 'bg-secondary'} text-xs sm:text-sm`"
                  >
                    <div :class="`w-5 h-5 sm:w-6 sm:h-6 rounded-full ${collab.color} flex items-center justify-center text-white text-xs font-medium shrink-0`">
                      {{ collab.initials }}
                    </div>
                    <!-- Display name instead of ID -->
                    <span class="text-xs break-all" :title="`${collab.name} (${collab.id})`">
                      {{ collab.name }}{{ collab.isCurrentUser ? ' (You)' : '' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- No collaborators message -->
            <div v-else class="text-center py-6 sm:py-8 text-muted-foreground">
              <p class="text-xs sm:text-sm">No collaborators in accessible tasks</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Tasks Title + Create Button (Desktop only) -->
      <div v-if="!loading && !error" class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <h2 class="text-2xl font-bold tracking-tight">Tasks</h2>
        <div class="hidden sm:block">
          <Button @click="handleCreateTask">Create New Task</Button>
        </div>
      </div>
      
      <DataTable v-if="!loading && !error" :data="transformedTasks" :columns="columns" />
      
      <!-- Mobile Create Button - Bottom of page -->
      <div class="block sm:hidden mt-4">
        <Button class="w-full" @click="handleCreateTask">Create Task</Button>
      </div>
    </div>
  </div>
</template>