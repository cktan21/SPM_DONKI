<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Label } from '@/components/ui/label'
import { ChevronDown, Calendar, Flag, FilePenLine, Trash2, Circle, Check, Loader, AlertTriangle } from 'lucide-vue-next'

interface Props {
  subtasks: any[]
  userId: string
  userRole: string
}

const props = defineProps<Props>()
const emit = defineEmits(['edit', 'delete'])
const router = useRouter()

const expandedSubtasks = ref<Set<string>>(new Set())

const toggleSubtask = (subtaskId: string) => {
  if (expandedSubtasks.value.has(subtaskId)) {
    expandedSubtasks.value.delete(subtaskId)
  } else {
    expandedSubtasks.value.add(subtaskId)
  }
}

const canEditSubtask = (subtask: any) => {
  return props.userRole === 'manager' || props.userId === subtask.created_by_uid
}

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
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardHeader class="pb-4">
      <div class="flex items-center justify-between">
        <div>
          <CardTitle class="text-base font-semibold text-slate-900 dark:text-slate-100">Subtasks</CardTitle>
          <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
            {{ subtasks?.length || 0 }} subtask{{ subtasks?.length !== 1 ? 's' : '' }}
          </CardDescription>
        </div>
      </div>
    </CardHeader>
    <CardContent>
      <div v-if="subtasks && subtasks.length > 0" class="space-y-2">
        <Collapsible
          v-for="sub in subtasks"
          :key="sub.id"
          class="group border border-slate-200 rounded-lg hover:shadow-sm hover:border-slate-300 transition-all dark:border-slate-800 dark:hover:border-slate-700"
          :open="expandedSubtasks.has(sub.id)"
          @update:open="() => toggleSubtask(sub.id)"
        >
          <div class="flex items-start gap-3 p-4">
            <CollapsibleTrigger as-child>
              <Button variant="ghost" size="sm" class="h-7 w-7 p-0 shrink-0 mt-0.5 hover:bg-slate-100 dark:hover:bg-slate-800">
                <ChevronDown 
                  class="h-4 w-4 transition-transform duration-200" 
                  :class="{ '-rotate-90': !expandedSubtasks.has(sub.id) }" 
                />
              </Button>
            </CollapsibleTrigger>
            
            <div class="flex-1 min-w-0 space-y-2">
              <div class="flex items-start justify-between gap-3">
                <button 
                  @click="router.push(`/task/${sub.id}`)"
                  class="font-medium text-sm leading-tight text-slate-900 dark:text-slate-100 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-left"
                >
                  {{ sub.name }}
                </button>
                <StatusBadge :status="sub.status" size="sm" />
              </div>
              
              <div class="flex flex-wrap items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
                <div class="flex items-center gap-1">
                  <Calendar class="w-3 h-3" />
                  <span>{{ formatDate(sub.deadline) }}</span>
                </div>
                <div v-if="sub.priorityLevel !== undefined && sub.priorityLevel !== null" class="flex items-center gap-1">
                  <Flag class="w-3 h-3" />
                  <span>Priority: {{ sub.priorityLevel }}</span>
                </div>
                <LabelBadge v-if="sub.label" :label="sub.label" size="xs" />
              </div>
            </div>

            <div v-if="canEditSubtask(sub)" class="flex gap-1 shrink-0">
              <Button 
                @click.stop="emit('edit', sub.id)" 
                size="icon" 
                variant="ghost" 
                class="h-8 w-8 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                <FilePenLine class="w-4 h-4 text-slate-600 dark:text-slate-400" />
              </Button>
              <Button 
                @click.stop="emit('delete', sub.id)" 
                size="icon" 
                variant="ghost" 
                class="h-8 w-8 hover:bg-red-50 text-red-600 dark:hover:bg-red-900/20"
              >
                <Trash2 class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <CollapsibleContent>
            <div class="px-4 pb-4 pt-2 border-t border-slate-100 bg-slate-50/50 dark:border-slate-800 dark:bg-slate-800/50">
              <div class="pl-10 space-y-3">
                <div v-if="sub.desc" class="space-y-1">
                  <Label class="text-xs font-medium text-slate-500 dark:text-slate-400">Description</Label>
                  <p class="text-sm text-slate-700 leading-relaxed dark:text-slate-300">{{ sub.desc }}</p>
                </div>
                <div v-if="sub.notes" class="space-y-1">
                  <Label class="text-xs font-medium text-slate-500 dark:text-slate-400">Notes</Label>
                  <p class="text-sm text-slate-700 leading-relaxed dark:text-slate-300">{{ sub.notes }}</p>
                </div>
              </div>
            </div>
          </CollapsibleContent>
        </Collapsible>
      </div>
      
      <div v-else class="flex flex-col items-center justify-center py-12 text-center">
        <div class="rounded-full bg-slate-100 p-3 mb-3 dark:bg-slate-800">
          <Circle class="w-6 h-6 text-slate-400 dark:text-slate-600" />
        </div>
        <p class="text-sm font-medium text-slate-600 dark:text-slate-400">No subtasks yet</p>
        <p class="text-xs text-slate-500 mt-1 dark:text-slate-500">Subtasks will appear here when created</p>
      </div>
    </CardContent>
  </Card>
</template>