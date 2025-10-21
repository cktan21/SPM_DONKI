<script setup lang="ts">
import { Check, Loader, AlertTriangle, Calendar } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'

defineProps<{
  subtask: {
    id: string | number
    title: string
    status?: string
    deadline?: string
  }
}>()

const getStatusIcon = (status: string) => {
  const statusLower = status.toLowerCase()
  if (statusLower === 'done') return Check
  if (statusLower === 'ongoing' || statusLower === 'in progress') return AlertTriangle
  return Loader
}

const getStatusClass = (status: string) => {
  const statusLower = status.toLowerCase()
  if (statusLower === 'done') {
    return 'bg-emerald-50 text-emerald-700 border-emerald-200'
  }
  if (statusLower === 'ongoing' || statusLower === 'in progress') {
    return 'bg-blue-50 text-blue-700 border-blue-200'
  }
  return 'bg-orange-50 text-orange-700 border-orange-200'
}

const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    'done': 'Done',
    'ongoing': 'Ongoing',
    'in progress': 'In Progress',
    'to do': 'To Do',
    'todo': 'To Do'
  }
  return statusMap[status.toLowerCase()] || status
}

const formatDeadline = (dateStr: string) => {
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return 'Invalid date'
  }
}
</script>

<template>
  <Card class="hover:bg-accent/50 transition-colors cursor-pointer border-border">
    <CardContent class="p-4">
      <div class="flex items-start justify-between gap-4">
        <!-- Left side: Title and metadata -->
        <div class="flex-1 min-w-0 space-y-2">
          <!-- Title - same font size as main table -->
          <h4 class="font-medium text-sm">
            {{ subtask.title }}
          </h4>
          
          <!-- Metadata row - same font size as main table -->
          <div class="flex items-center gap-4 text-sm text-muted-foreground">
            <!-- Task ID - FULL ID NO TRUNCATION -->
            <div class="flex items-center gap-1.5">
              <span class="font-normal">Task ID:</span>
              <span class="font-mono">{{ subtask.id }}</span>
            </div>
            
            <!-- Deadline -->
            <div class="flex items-center gap-1.5">
              <Calendar :size="14" class="shrink-0" />
              <span class="font-normal">Deadline:</span>
              <span v-if="subtask.deadline">{{ formatDeadline(subtask.deadline) }}</span>
              <span v-else>Not set</span>
            </div>
          </div>
        </div>
        
        <!-- Right side: Status Badge - SAME SIZE AS MAIN TABLE -->
        <div class="shrink-0">
          <Badge 
            v-if="subtask.status"
            variant="outline"
            :class="`${getStatusClass(subtask.status)} border h-5 px-2 text-xs font-medium rounded-full`"
          >
            <component :is="getStatusIcon(subtask.status)" class="h-3 w-3 mr-1" />
            {{ formatStatus(subtask.status) }}
          </Badge>
          <Badge 
            v-else
            variant="outline"
            class="bg-gray-50 text-gray-600 border-gray-200 h-5 px-2 text-xs font-medium rounded-full"
          >
            No Status
          </Badge>
        </div>
      </div>
    </CardContent>
  </Card>
</template>