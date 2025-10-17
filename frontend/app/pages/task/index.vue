<script setup lang="ts">
import { columns } from './components/columns'
import tasks from './data/tasks.json'
import DataTable from './components/DataTable.vue'
import SubtaskItem from './components/SubtaskItem.vue'
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'

const router = useRouter()

// Transform tasks to match expected type
const transformedTasks = tasks.map(task => ({
  id: String(task.id), // Ensure id is string
  status: task.status || '',
  title: task.title || '',
  label: task.label || '',
  priority: task.priority || 0,
  // Include optional fields if needed
  subtasks: task.subtasks,
  progress: task.progress,
  due_date: task.due_date
}))

const handleCreateTask = () => {
  router.push('/task/create')
}
</script>

<template>
  <div class="container mx-auto py-10 px-3">
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div class="w-full sm:w-auto">
          <h1 class="text-3xl font-bold tracking-tight">Tasks</h1>
          <p class="text-muted-foreground w-full sm:w-auto">
            Manage your tasks and view their details
          </p>
        </div>
        <div class="hidden sm:block">
          <Button @click="handleCreateTask">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="mr-2">
              <path d="M5 12h14" />
              <path d="M12 5v14" />
            </svg>
            Create Task
          </Button>
        </div>
      </div>

      <!-- Data table -->
      <DataTable :data="transformedTasks" :columns="columns" />

      <!-- Mobile create button -->
      <div class="block sm:hidden mt-4">
        <Button class="w-full" @click="handleCreateTask">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
               viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
               class="mr-2">
            <path d="M5 12h14" />
            <path d="M12 5v14" />
          </svg>
          Create Task
        </Button>
      </div>
    </div>
  </div>
</template>
