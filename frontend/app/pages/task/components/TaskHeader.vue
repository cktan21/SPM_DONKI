<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { FilePenLine, Trash2, Clock, User, Check, Loader, AlertTriangle, AlertCircle } from 'lucide-vue-next'

interface Props {
  task: any
  canEdit: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['edit', 'delete'])

const formatDateShort = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } catch {
    return 'N/A'
  }
}

const getStatusConfig = (status: string) => {
  const normalized = (status || '').toLowerCase()
  if (normalized === 'overdue' || normalized === 'Blocked') {
    return {
      label: 'Overdue',
      icon: AlertCircle,
      class: 'bg-red-50 text-red-700 border-red-200 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20',
    }
  }
  if (normalized === 'done' || normalized === 'completed') {
    return {
      label: 'Done',
      icon: Check,
      class: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20',
    }
  }
  
  if (normalized === 'ongoing') {
    return {
      label: 'Ongoing',
      icon: AlertTriangle,
      class: 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20',
    }
  }
  
  return {
    label: 'To Do',
    icon: Loader,
    class: 'bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20',
  }
}

const statusConfig = computed(() => getStatusConfig(props.task.status))
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardHeader class="space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div class="flex-1 space-y-3">
          <CardTitle class="text-3xl font-semibold tracking-tight text-slate-900 dark:text-slate-50">
            {{ task.name || 'Untitled Task' }}
          </CardTitle>
          <div class="flex flex-wrap items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
            <div class="flex items-center gap-1.5">
              <Clock class="w-3.5 h-3.5" />
              <span>Updated {{ formatDateShort(task.updated_timestamp) }}</span>
            </div>
            <span class="text-slate-300 dark:text-slate-700">•</span>
            <div v-if="task.created_by" class="flex items-center gap-1.5">
              <User class="w-3.5 h-3.5" />
              <span>{{ task.created_by?.name }}</span>
            </div>
          </div>
        </div>
        <div v-if="canEdit" class="flex gap-2 shrink-0">
          <Button
            @click="emit('edit')"
            size="sm"
            variant="outline"
            class="gap-2 border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800"
          >
            <FilePenLine class="w-4 h-4" />
            <span class="hidden sm:inline">Edit</span>
          </Button>
          <Button
            @click="emit('delete')"
            size="sm"
            variant="outline"
            class="gap-2 text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700 dark:border-red-900 dark:hover:bg-red-950"
          >
            <Trash2 class="w-4 h-4" />
            <span class="hidden sm:inline">Delete</span>
          </Button>
        </div>
      </div>

      <!-- Status Badge -->
      <Badge
        :class="`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border font-medium text-sm w-fit ${statusConfig.class}`"
      >
        <component :is="statusConfig.icon" class="h-3.5 w-3.5" />
        {{ statusConfig.label }}
      </Badge>
    </CardHeader>
  </Card>
</template>