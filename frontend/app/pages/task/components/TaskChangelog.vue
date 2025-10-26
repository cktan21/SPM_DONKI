<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Stepper, StepperItem, StepperSeparator, StepperTrigger, StepperTitle, StepperDescription } from '@/components/ui/stepper'
import { Check, Circle, Dot } from 'lucide-vue-next'

interface Props {
  changelog: any[]
}

const props = defineProps<Props>()

const formatChangelogDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    const date = new Date(dateStr)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${day}/${month}/${year} at ${hours}:${minutes}`
  } catch {
    return 'N/A'
  }
}

const getChangeDescription = (log: any) => {
  const operation = log.operation?.toLowerCase()
  const tableName = log.table_name?.toLowerCase()
  
  if (operation === 'insert') {
    if (tableName === 'task') return 'Task created'
    if (tableName === 'schedule') return 'Schedule initialized'
    return 'Record created'
  }
  
  if (operation === 'update') {
    const changedFields = log.changed_fields || []
    const delta = log.delta || {}
    
    if (changedFields.length === 0) return 'Updated'
    
    const descriptions = []
    
    for (const field of changedFields) {
      if (field === 'status' && delta[field]) {
        const oldStatus = delta[field].old || 'unknown'
        const newStatus = delta[field].new || 'unknown'
        descriptions.push(`Status changed from "${oldStatus}" to "${newStatus}"`)
      } else if (field === 'label' && delta[field]) {
        const oldLabel = delta[field].old || 'none'
        const newLabel = delta[field].new || 'none'
        descriptions.push(`Label changed from "${oldLabel}" to "${newLabel}"`)
      } else if (field === 'desc') {
        descriptions.push('Description updated')
      } else if (field === 'name' && delta[field]) {
        descriptions.push(`Renamed to "${delta[field].new}"`)
      } else if (field === 'collaborators' && delta[field]) {
        const oldCount = delta[field].old?.length || 0
        const newCount = delta[field].new?.length || 0
        if (newCount > oldCount) {
          descriptions.push(`Added ${newCount - oldCount} collaborator(s)`)
        } else if (newCount < oldCount) {
          descriptions.push(`Removed ${oldCount - newCount} collaborator(s)`)
        } else {
          descriptions.push('Collaborators updated')
        }
      } else if (field === 'deadline' && delta[field]) {
        descriptions.push('Deadline updated')
      } else if (field === 'priorityLevel' && delta[field]) {
        descriptions.push(`Priority changed to P${delta[field].new}`)
      } else if (field !== 'updated_timestamp' && field !== 'created_at') {
        descriptions.push(`${field.charAt(0).toUpperCase() + field.slice(1)} updated`)
      }
    }
    
    return descriptions.length > 0 ? descriptions.join(', ') : 'Updated'
  }
  
  if (operation === 'delete') return 'Deleted'
  
  return operation || 'Changed'
}

const processedChangelog = computed(() => {
  if (!props.changelog || props.changelog.length === 0) return []
  
  return props.changelog
    .sort((b, a) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
    .map((log, index, array) => ({
      step: index + 1,
      title: getChangeDescription(log),
      timestamp: formatChangelogDate(log.timestamp),
      status: index === array.length - 1 ? 'active' : 'completed',
      operation: log.operation,
      tableName: log.table_name
    }))
})
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardHeader class="pb-4">
      <CardTitle class="text-base font-semibold text-slate-900 dark:text-slate-100">Activity</CardTitle>
      <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
        Track all changes made to this task
      </CardDescription>
    </CardHeader>
    <CardContent>
      <div v-if="processedChangelog.length > 0">
        <Stepper orientation="vertical" class="flex flex-col justify-start gap-6">
          <StepperItem
            v-for="change in processedChangelog"
            :key="change.step"
            v-slot="{ state }"
            class="relative flex items-start gap-4"
            :step="change.step"
          >
            <StepperSeparator
              v-if="change.step !== processedChangelog[processedChangelog.length - 1]?.step"
              class="absolute left-[18px] top-[38px] block h-[calc(100%+0.5rem)] w-0.5 shrink-0 rounded-full bg-slate-200 dark:bg-slate-800 group-data-[state=completed]:bg-blue-500"
            />
            <StepperTrigger as-child>
              <Button
                :variant="state === 'completed' || state === 'active' ? 'default' : 'outline'"
                size="icon"
                class="z-10 rounded-full shrink-0 h-9 w-9 shadow-sm"
                :class="[
                  state === 'active' && 'ring-2 ring-blue-500 ring-offset-2 ring-offset-background',
                  state === 'completed' && 'bg-blue-600 hover:bg-blue-700'
                ]"
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
                class="text-xs text-slate-500 transition dark:text-slate-500"
              >
                {{ change.timestamp }}
              </StepperDescription>
            </div>
          </StepperItem>
        </Stepper>
      </div>
      <div v-else class="flex flex-col items-center justify-center py-12 text-center">
        <div class="rounded-full bg-slate-100 p-3 mb-3 dark:bg-slate-800">
          <Circle class="w-6 h-6 text-slate-400 dark:text-slate-600" />
        </div>
        <p class="text-sm font-medium text-slate-600 dark:text-slate-400">No activity yet</p>
        <p class="text-xs text-slate-500 mt-1 dark:text-slate-500">Changes will appear here as they happen</p>
      </div>
    </CardContent>
  </Card>
</template>