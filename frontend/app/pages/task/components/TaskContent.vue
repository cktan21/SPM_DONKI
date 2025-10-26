<script setup lang="ts">
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'

interface Props {
  task: any
}

defineProps<Props>()
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardContent class="p-6 space-y-6">
      <!-- Description -->
      <div class="space-y-2">
        <Label class="text-xs font-semibold text-slate-500 uppercase tracking-wider dark:text-slate-400">
          Description
        </Label>
        <div class="text-sm text-slate-700 leading-relaxed dark:text-slate-300 whitespace-pre-wrap">
          {{ task.desc || 'No description provided.' }}
        </div>
      </div>

      <!-- Notes -->
      <div class="space-y-2">
        <Label class="text-xs font-semibold text-slate-500 uppercase tracking-wider dark:text-slate-400">
          Notes
        </Label>
        <div class="text-sm text-slate-700 leading-relaxed dark:text-slate-300 whitespace-pre-wrap">
          {{ task.notes || 'No notes provided.' }}
        </div>
      </div>
    </CardContent>
  </Card>
</template>