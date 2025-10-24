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

// Get current user data from middleware
const userData = useState<any>('userData')

// Get current user ID
const currentUserId = computed(() => {
  return userData.value?.user?.id || null
})

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
    console.log('Current user ID:', currentUserId.value)
  } catch (err: any) {
    console.error('Error fetching project:', err)
    error.value = err.message || 'Failed to fetch project'
  } finally {
    loading.value = false
  }
}

// Helper function to check if user has access to a task
const canUserAccessTask = (task: Task): boolean => {
  console.log('\n--- Checking Access for Task:', task.name, '---')
  console.log('1) My User ID:', currentUserId.value)
  
  if (!currentUserId.value) {
    console.warn('No current user ID found')
    return false
  }

  // Case 1: User is the creator
  console.log('Task Creator ID:', task.created_by_uid)
  console.log('Am I the creator?', task.created_by_uid === currentUserId.value)
  
  if (task.created_by_uid === currentUserId.value) {
    console.log(`✓ User is creator of task: ${task.name}`)
    return true
  }

  // Case 2: User is a collaborator
  if (task.collaborators && Array.isArray(task.collaborators)) {
    console.log('2) Checking collaborators array...')
    console.log('Total collaborators:', task.collaborators.length)
    
    let isCollaborator = false
    task.collaborators.forEach((collab, index) => {
      if (collab) {
        console.log(`   Collaborator ${index + 1}:`)
        console.log(`   - Collaborator ID: ${collab.id}`)
        console.log(`   - Collaborator Name: ${collab.name}`)
        const isMatch = collab.id === currentUserId.value
        console.log(`   3) Is my user ID same as this collaborator ID? ${isMatch}`)
        if (isMatch) {
          isCollaborator = true
        }
      }
    })
    
    if (isCollaborator) {
      console.log(`✓ User is collaborator on task: ${task.name}`)
      return true
    }
  } else {
    console.log('No collaborators array or empty array')
  }

  // Case 3: User is neither creator nor collaborator
  console.log(`✗ User has no access to task: ${task.name}`)
  return false
}

// Filter tasks based on user access
const accessibleTasks = computed(() => {
  if (!selectedProject.value?.tasks || !currentUserId.value) {
    return []
  }
  
  const filtered = selectedProject.value.tasks.filter(task => canUserAccessTask(task))
  console.log('\n=== ACCESSIBLE TASKS SUMMARY ===')
  console.log('Total tasks in project:', selectedProject.value.tasks.length)
  console.log('Accessible tasks after filtering:', filtered.length)
  console.log('Accessible task names:', filtered.map(t => t.name))
  
  return filtered
})

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
    console.log('Current user ID:', currentUserId.value)
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

// Separate main tasks from subtasks (ONLY from accessible tasks)
const mainTasks = computed(() => {
  if (!accessibleTasks.value.length) return []
  // Only return tasks that don't have a parentTaskId
  const mains = accessibleTasks.value.filter(task => !task.parentTaskId)
  
  console.log('\n=== MAIN TASKS vs SUBTASKS ===')
  console.log('Main tasks (no parentTaskId):', mains.length)
  console.log('Main task names:', mains.map(t => t.name))
  
  const subs = accessibleTasks.value.filter(task => task.parentTaskId)
  console.log('Subtasks (have parentTaskId):', subs.length)
  console.log('Subtask names:', subs.map(t => `${t.name} (parent: ${t.parentTaskId})`))
  
  return mains
})

const subtasksByParentId = computed(() => {
  if (!accessibleTasks.value.length) return {}
  
  const map: Record<string, Task[]> = {}
  accessibleTasks.value.forEach(task => {
    const parentId = task.parentTaskId
    if (parentId) {
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
    })) || []
  }))
})

// Calculate progress data from ALL ACCESSIBLE TASKS (including subtasks)
const progressData = computed(() => {
  if (!accessibleTasks.value.length) {
    return { done: 0, ongoing: 0, toDo: 0, total: 0 }
  }

  // Count ALL accessible tasks (both main tasks and subtasks)
  const tasks = accessibleTasks.value
  const done = tasks.filter(t => t.status === 'done').length
  const ongoing = tasks.filter(t => t.status === 'ongoing').length
  const toDo = tasks.filter(t => t.status === 'to do').length
  const total = tasks.length

  console.log('\n=== PROGRESS CALCULATION ===')
  console.log('Total accessible tasks (main + subtasks):', total)
  console.log('Done:', done)
  console.log('Ongoing:', ongoing)
  console.log('To Do:', toDo)

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

// Get unique collaborators from ACCESSIBLE tasks only (including creators)
const uniqueCollaborators = computed(() => {
  if (!accessibleTasks.value.length) return []

  const collabMap = new Map<string, { id: string; name: string }>()
  
  accessibleTasks.value.forEach(task => {
    // Add the task creator
    if (task.created_by_uid) {
      // Try to get creator info from the task's created_by field if it exists
      const creatorInfo = (task as any).created_by
      if (creatorInfo && creatorInfo.id && creatorInfo.name) {
        collabMap.set(creatorInfo.id, { id: creatorInfo.id, name: creatorInfo.name })
      } else {
        // If no created_by info, just use the UID (we'll need to handle the name)
        if (!collabMap.has(task.created_by_uid)) {
          // Try to find the creator's name from other tasks or collaborators
          const existingEntry = collabMap.get(task.created_by_uid)
          if (!existingEntry) {
            collabMap.set(task.created_by_uid, { 
              id: task.created_by_uid, 
              name: 'Task Creator' // Fallback name
            })
          }
        }
      }
    }
    
    // Add collaborators
    if (task.collaborators && Array.isArray(task.collaborators)) {
      task.collaborators.forEach(collab => {
        if (collab && typeof collab === 'object' && 'id' in collab && 'name' in collab) {
          const collaborator = collab as { id: string; name: string }
          collabMap.set(collaborator.id, { id: collaborator.id, name: collaborator.name })
        }
      })
    }
  })

  return Array.from(collabMap.values()).map((collab, index) => ({
    id: collab.id,
    name: collab.name,
    initials: getInitialsFromName(collab.name),
    color: getColorForIndex(index)
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
            Manage your tasks and view their details
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8 text-muted-foreground">
        Loading project...
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8 text-destructive">
        {{ error }}
      </div>

      <!-- No User ID Warning -->
      <div v-else-if="!currentUserId" class="text-center py-8 text-destructive">
        Unable to load user information. Please log in again.
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
                    :class="`w-8 h-8 sm:w-10 sm:h-10 rounded-full ${collab.color} flex items-center justify-center text-white text-xs sm:text-sm font-medium border-2 border-white hover:z-10 transition-transform hover:scale-110 cursor-pointer`"
                    :title="collab.name"
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
                    class="inline-flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-secondary text-xs sm:text-sm"
                  >
                    <div :class="`w-5 h-5 sm:w-6 sm:h-6 rounded-full ${collab.color} flex items-center justify-center text-white text-xs font-medium shrink-0`">
                      {{ collab.initials }}
                    </div>
                    <!-- Display name instead of ID -->
                    <span class="text-xs break-all" :title="`${collab.name} (${collab.id})`">{{ collab.name }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- No collaborators message -->
            <div v-else class="text-center py-6 sm:py-8 text-muted-foreground">
              <p class="text-xs sm:text-sm">No collaborators in this project yet</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Tasks Title + Create Button (Desktop only) -->
      <div v-if="!loading && !error && currentUserId" class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <h2 class="text-2xl font-bold tracking-tight">Tasks</h2>
        <div class="hidden sm:block">
          <Button @click="handleCreateTask">Create New Task</Button>
        </div>
      </div>
      
      <DataTable v-if="!loading && !error && currentUserId" :data="transformedTasks" :columns="columns" />
      
      <!-- Mobile Create Button - Bottom of page -->
      <div v-if="!loading && !error && currentUserId" class="block sm:hidden mt-4">
        <Button class="w-full" @click="handleCreateTask">Create Task</Button>
      </div>
    </div>
  </div>
</template>