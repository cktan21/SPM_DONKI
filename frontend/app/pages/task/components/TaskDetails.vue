<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { Calendar, Flag, Tag, RefreshCw, FolderOpen, User } from 'lucide-vue-next'

interface Props {
  task: any
}

const props = defineProps<Props>()
const router = useRouter()

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    const date = new Date(dateStr)
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    return `${day}/${month}/${year}`
  } catch {
    return 'N/A'
  }
}

const getColorFromName = (name: string) => {
  const colors = [
    'bg-red-600', 'bg-blue-600', 'bg-green-600', 'bg-amber-600',
    'bg-purple-600', 'bg-pink-600', 'bg-indigo-600', 'bg-teal-600',
  ]
  const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return colors[hash % colors.length]
}

const getInitials = (name: string | undefined) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardHeader class="pb-3">
      <CardTitle class="text-base font-semibold">Details</CardTitle>
    </CardHeader>
    <CardContent class="space-y-5">
      <!-- Deadline -->
      <div class="space-y-1.5">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <Calendar class="w-3.5 h-3.5" />
          Deadline
        </div>
        <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
          {{ formatDate(task.deadline) }}
        </p>
      </div>

      <Separator class="bg-slate-100 dark:bg-slate-800" />

      <!-- Priority -->
      <div class="space-y-1.5">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <Flag class="w-3.5 h-3.5" />
          Priority
        </div>
        <Badge 
          v-if="task.priorityLevel !== undefined && task.priorityLevel !== null" 
          variant="outline"
          class="text-xs font-medium bg-orange-50 text-orange-700 border-orange-200 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20"
        >
          {{ task.priorityLevel }}
        </Badge>
        <p v-else class="text-sm text-slate-600 dark:text-slate-400">Not set</p>
      </div>

      <Separator v-if="task.label" class="bg-slate-100 dark:bg-slate-800" />

      <!-- Label -->
      <div v-if="task.label" class="space-y-1.5">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <Tag class="w-3.5 h-3.5" />
          Label
        </div>
        <Badge variant="outline" class="capitalize text-xs font-medium bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-500/10 dark:text-purple-400 dark:border-purple-500/20">
          {{ task.label }}
        </Badge>
      </div>

      <Separator class="bg-slate-100 dark:bg-slate-800" />

      <!-- Project -->
      <div class="space-y-1.5">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <FolderOpen class="w-3.5 h-3.5" />
          Project
        </div>
        <p class="text-sm font-medium text-slate-900 dark:text-slate-100">
          {{ task.project?.name || 'No Project' }}
        </p>
      </div>

      <Separator v-if="task.parent_task" class="bg-slate-100 dark:bg-slate-800" />

      <!-- Parent Task -->
      <div v-if="task.parent_task" class="space-y-1.5">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <FolderOpen class="w-3.5 h-3.5" />
          Parent Task
        </div>
        <button
          @click="router.push(`/task/${task.parent_task.id}`)"
          class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 hover:underline text-left"
        >
          {{ task.parent_task.name || 'View Parent' }}
        </button>
      </div>

      <Separator class="bg-slate-100 dark:bg-slate-800" />

      <!-- Collaborators -->
      <div class="space-y-3">
        <div class="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400">
          <User class="w-3.5 h-3.5" />
          Collaborators
        </div>
        <div v-if="task.collaborators?.length" class="space-y-2">
          <div
            v-for="(collab, idx) in task.collaborators"
            :key="idx"
            class="flex items-center gap-2.5"
          >
            <Avatar class="h-8 w-8 border border-slate-200 dark:border-slate-800">
              <AvatarFallback :class="`text-black text-xs font-medium ${getColorFromName(collab?.name || collab)}`">
                {{ getInitials(collab?.name || collab) }}
              </AvatarFallback>
            </Avatar>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-slate-900 truncate dark:text-slate-100">
                {{ typeof collab === 'string' ? collab : (collab?.name || 'Unknown') }}
              </p>
            </div>
          </div>
        </div>
        <p v-else class="text-sm text-slate-600 dark:text-slate-400">None</p>
      </div>
    </CardContent>
  </Card>
</template>