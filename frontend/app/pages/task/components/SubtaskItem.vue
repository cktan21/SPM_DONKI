<template>
  <div
    class="flex flex-col sm:flex-row sm:items-center justify-between border rounded-lg p-3 mb-2 bg-card hover:bg-muted/50 transition"
  >
    <div>
      <p class="font-medium">{{ subtask.title }}</p>
      <p class="text-sm text-muted-foreground">
        ID: {{ subtask.id }}
      </p>
      <p class="text-sm text-muted-foreground">
        Status: {{ subtask.status ?? 'N/A' }}
      </p>
      <p class="text-sm text-muted-foreground">
        Deadline:
        {{ subtask.deadline ? new Date(subtask.deadline).toLocaleString() : 'N/A' }}
      </p>
    </div>

    <!-- Optional control slot for buttons or status toggles -->
    <div class="mt-2 sm:mt-0 flex gap-2 items-center">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  subtask: {
    id: string | number
    title: string
    status?: string
    deadline?: string
  }
}>()
</script>