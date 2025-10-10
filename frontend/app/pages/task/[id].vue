<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const taskId = computed(() => route.params.id)
</script>

<template>
  <div class="container mx-auto py-10">
    <div class="space-y-6">
      <!-- Back button -->
      <div>
        <button 
          @click="$router.back()"
          class="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground"
        >
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
            <path d="m15 18-6-6 6-6"/>
          </svg>
          Back to tasks
        </button>
      </div>

      <!-- Task detail card -->
      <div class="rounded-lg border bg-card p-6">
        <h1 class="text-3xl font-bold mb-4">Task Detail</h1>
        <div class="space-y-4">
          <div>
            <p class="text-sm text-muted-foreground">Task ID</p>
            <p class="text-2xl font-semibold">{{ taskId }}</p>
          </div>
          
          <div class="pt-4 border-t">
            <p class="text-muted-foreground">
              This is a placeholder page for task details. 
              You can now fetch and display the full task information here.
            </p>
          </div>
        </div>
      </div>

      <!-- Placeholder for additional content -->
      <div class="rounded-lg border bg-card p-6">
        <h2 class="text-xl font-semibold mb-2">Task Information</h2>
        <p class="text-muted-foreground">
          Add your task details, status, priority, and other information here.
        </p>
      </div>
    </div>
  </div>
</template>