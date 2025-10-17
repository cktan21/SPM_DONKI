<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { columns } from './components/columns'
import tasks from './data/tasks.json'
import DataTable from './components/DataTable.vue'
import { Button } from '@/components/ui/button'
import { computed } from 'vue'

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

// Transform tasks for table
const transformedTasks = tasks.map(task => ({
  id: String(task.id),
  status: task.status || '',
  title: task.title || '',
  label: task.label || '',
  priority: task.priority || 0,
  subtasks: task.subtasks,
  progress: task.progress,
  due_date: task.due_date
}))

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
