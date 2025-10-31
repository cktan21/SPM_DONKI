<script setup lang="ts">
import { ref, computed } from 'vue'
import { Calendar, Flag, Check, Loader, AlertTriangle } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Button } from '@/components/ui/button'

const props = defineProps<{
  subtask: {
    id: string | number
    title: string
    status?: string | null
    deadline?: string | null
    label?: string | null
    priority?: number
  }
}>()

// Label options and state
const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

const currentLabel = ref(props.subtask.label)
const isLabelOpen = ref(false)
const isLabelUpdating = ref(false)

const updateLabel = async (newLabel: string) => {
  if (isLabelUpdating.value || newLabel === currentLabel.value) return
  
  isLabelUpdating.value = true
  
  try {
    const taskId = props.subtask.id
    const response = await fetch(`http://127.0.0.1:4000/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ label: newLabel })
    })
    
    if (!response.ok) throw new Error('Failed to update label')
    
    currentLabel.value = newLabel
    isLabelOpen.value = false
    
    console.log('Label updated successfully')
  } catch (error) {
    console.error('Error updating label:', error)
  } finally {
    isLabelUpdating.value = false
  }
}

// Status options and state
const statuses = [
  { 
    value: "to do", 
    label: "To Do", 
    icon: Loader, 
    class: "bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100 dark:bg-orange-500/10 dark:text-orange-400 dark:border-orange-500/20 dark:hover:bg-orange-500/20"
  },
  { 
    value: "ongoing", 
    label: "Ongoing", 
    icon: AlertTriangle, 
    class: "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20 dark:hover:bg-blue-500/20"
  },
  { 
    value: "overdue", 
    label: "Overdue", 
    icon: AlertTriangle, 
    class: "bg-red-50 text-red-700 border-red-200 hover:bg-blue-100 dark:bg-blue-500/10 dark:text-blue-400 dark:border-blue-500/20 dark:hover:bg-blue-500/20"
  },
  { 
    value: "done", 
    label: "Done", 
    icon: Check, 
    class: "bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20 dark:hover:bg-emerald-500/20"
  },
] as const

const currentStatus = ref(props.subtask.status)
const isStatusOpen = ref(false)
const isStatusUpdating = ref(false)

const currentStatusStyle = computed(() => {
  const statusValue = currentStatus.value
  if (!statusValue) return statuses[0]
  const found = statuses.find(s => s.value === statusValue)
  return found ?? statuses[0]
})

const updateStatus = async (newStatus: string) => {
  if (isStatusUpdating.value || newStatus === currentStatus.value) return
  
  isStatusUpdating.value = true
  
  try {
    const taskId = props.subtask.id
    const response = await fetch(`http://127.0.0.1:4000/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    
    if (!response.ok) throw new Error('Failed to update status')
    
    currentStatus.value = newStatus
    isStatusOpen.value = false
    
    console.log('Status updated successfully')
  } catch (error) {
    console.error('Error updating status:', error)
  } finally {
    isStatusUpdating.value = false
  }
}

// Priority configuration
const getPriorityConfig = (priority: number) => {
  const configs = {
    1: { 
      label: 'Low',
      class: 'bg-blue-50 text-blue-700 border-blue-200/50',
      dotClass: 'bg-blue-500'
    },
    2: { 
      label: 'Medium',
      class: 'bg-amber-50 text-amber-700 border-amber-200/50',
      dotClass: 'bg-amber-500'
    },
    3: { 
      label: 'High',
      class: 'bg-orange-50 text-orange-700 border-orange-200/50',
      dotClass: 'bg-orange-500'
    },
    4: { 
      label: 'Urgent',
      class: 'bg-red-50 text-red-700 border-red-200/50',
      dotClass: 'bg-red-500'
    }
  }
  return configs[priority as keyof typeof configs] || configs[1]
}

const formatDeadline = (dateStr: string) => {
  try {
    const date = new Date(dateStr)
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const deadlineDate = new Date(date)
    deadlineDate.setHours(0, 0, 0, 0)
    
    const diffTime = deadlineDate.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    // Format as DD/MM/YYYY
    const day = String(date.getDate()).padStart(2, '0')
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const year = date.getFullYear()
    const formattedDate = `${day}/${month}/${year}`
    
    if (diffDays < 0) {
      return { text: formattedDate, overdue: true }
    } else if (diffDays === 0) {
      return { text: 'Today', urgent: true }
    } else if (diffDays === 1) {
      return { text: 'Tomorrow', urgent: true }
    } else if (diffDays <= 7) {
      return { text: formattedDate, soon: true }
    }
    
    return { text: formattedDate, normal: true }
  } catch {
    return { text: 'Invalid date', normal: true }
  }
}
</script>

<template>
  <Card class="group hover:shadow-md hover:border-primary/20 transition-all duration-200 border-border/60 bg-card/50 backdrop-blur-sm">
    <CardContent class="p-4">
      <div class="space-y-3">
        <!-- Header: Title -->
        <div class="flex items-start justify-between gap-3">
          <h4 class="font-semibold text-sm text-foreground leading-snug flex-1">
            {{ subtask.title }}
          </h4>
        </div>

        <!-- Badges Row: Status, Label, Priority -->
        <div class="flex flex-wrap items-center gap-2">
          <!-- Status Badge -->
          <Popover v-if="currentStatus" v-model:open="isStatusOpen">
            <PopoverTrigger as-child>
              <Button 
                variant="ghost" 
                :class="`h-7 py-0 px-2.5 rounded-md border text-xs font-medium transition-all ${currentStatusStyle.class}`"
                @click.stop
                :disabled="isStatusUpdating"
              >
                <component 
                  :is="currentStatusStyle.icon" 
                  class="h-3 w-3 mr-1.5" 
                />
                {{ currentStatusStyle.label }}
              </Button>
            </PopoverTrigger>
            <PopoverContent class="w-40 p-1.5 shadow-lg border-slate-200 dark:border-slate-800" align="start" @click.stop>
              <div class="space-y-0.5">
                <Button
                  v-for="status in statuses"
                  :key="status.value"
                  variant="ghost"
                  size="sm"
                  :class="`w-full justify-start text-xs h-8 rounded-md ${
                    status.value === currentStatus 
                      ? 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100' 
                      : 'hover:bg-slate-50 dark:hover:bg-slate-900'
                  }`"
                  :disabled="isStatusUpdating"
                  @click="updateStatus(status.value)"
                >
                  <component :is="status.icon" class="h-3.5 w-3.5 mr-2" />
                  {{ status.label }}
                </Button>
              </div>
            </PopoverContent>
          </Popover>

          <!-- Label Badge - Auto-populated from data -->
          <Badge
            v-if="currentLabel"
            variant="outline"
            class="capitalize px-2.5 py-1 text-xs font-medium bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-500/10 dark:text-purple-400 dark:border-purple-500/20"
          >
            {{ labels.find(l => l.value === currentLabel)?.label || currentLabel }}
          </Badge>

          <!-- Priority Badge - Simple white card with black border -->
          <Badge 
            v-if="subtask.priority"
            variant="outline"
            class="border-slate-300 bg-white text-slate-900 px-2.5 py-0.5 text-xs font-medium inline-flex items-center gap-1.5"
          >
            <Flag :size="12" class="shrink-0" />
            Priority: {{ subtask.priority }}
          </Badge>
        </div>

        <!-- Metadata Row: Project ID and Deadline (both on left) -->
        <div class="flex items-center gap-4 pt-2 border-t border-border/40">
          <!-- Project ID -->
          <div class="flex items-center gap-2 text-xs text-muted-foreground">
            <span class="font-medium opacity-60">Project ID</span>
            <span class="font-mono text-foreground/70 tracking-tight">{{ subtask.id }}</span>
          </div>
          
          <!-- Deadline - No colors -->
          <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Calendar :size="13" class="shrink-0" />
            <span class="font-medium opacity-60">Deadline:</span>
            <span v-if="subtask.deadline">{{ formatDeadline(subtask.deadline).text }}</span>
            <span v-else>Not set</span>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>