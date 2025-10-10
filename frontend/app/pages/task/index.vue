<script setup lang="ts">
import { h } from 'vue'
import { columns } from './components/columns'
import tasks from './data/tasks.json'
import DataTable from './components/DataTable.vue'
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleCreateTask = () => {
  router.push('/task/create')
}
</script>

<template>
  <div class="container mx-auto py-10">
    <div class="space-y-6">
      <!-- Header section with title and create button -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold tracking-tight">Tasks</h1>
          <p class="text-muted-foreground">
            Manage your tasks and view their details
          </p>
        </div>
        <Button @click="handleCreateTask">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width="16" 
            height="16" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round"
            class="mr-2"
          >
            <path d="M5 12h14"/>
            <path d="M12 5v14"/>
          </svg>
          Create Task
        </Button>
      </div>

      <!-- Data table -->
      <DataTable :data="tasks" :columns="columns" />
    </div>
  </div>
</template>