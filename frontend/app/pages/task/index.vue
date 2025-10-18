<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { columns } from './components/columns'
import DataTable from './components/DataTable.vue'
import { Button } from '@/components/ui/button'

// Task and Project interfaces
interface Task {
  id: string
  name: string
  created_by_uid: string
  updated_timestamp: string
  parentTaskId: string | null
  collaborators: string[] | null
  pid: string
  desc: string
  notes: string
  priorityLevel: number
  priorityLabel: string
  // Add these fields to your backend/API if not present
  label?: string | null

  // These fields come from SCHEDULE table but are flattened into task
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

// Fetch selected project from global state
const selectedProject = useState<Project | null>('selectedProject')

// Log the project if available
onMounted(() => {
  if (selectedProject.value) {
    console.log('Received project object:', selectedProject.value)
  } else {
    console.warn('No project selected. Go back and select a project first.')
  }
})

// Transform tasks from selectedProject for the table
const transformedTasks = computed(() => {
  if (!selectedProject.value?.tasks) {
    return []
  }

  return selectedProject.value.tasks.map(task => ({
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
    title: task.name, // Map 'name' to 'title' for the table
    priority: task.priorityLevel, // Map 'priorityLevel' to 'priority' for the table
    status: task.status || null, // Set to null if you don't have status in API yet
    label: task.label || null, // Set to null if you don't have label in API yet
  }))
})

const projectTitle = computed(() =>
  selectedProject.value
    ? `${selectedProject.value.name}'s Tasks`
    : 'Tasks'
)

const handleCreateTask = () => {
  router.push('/task/create')
}
</script>

<template>
  <div class="container mx-auto py-10 px-3">
    <div class="space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div class="w-full sm:w-auto">
          <h1 class="text-3xl font-bold tracking-tight">
            {{ projectTitle }}
          </h1>
          <p class="text-muted-foreground w-full sm:w-auto">
            Manage your tasks and view their details
          </p>
        </div>
        <div class="hidden sm:block">
          <Button @click="handleCreateTask">Create New Task</Button>
        </div>
      </div>
      
      <DataTable :data="transformedTasks" :columns="columns" />
      
      <div class="block sm:hidden mt-4">
        <Button class="w-full" @click="handleCreateTask">Create Task</Button>
      </div>
    </div>
  </div>
</template>