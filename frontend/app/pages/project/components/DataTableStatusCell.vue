<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Row } from '@tanstack/vue-table'
import type { Task } from '../data/schema'
import { Check, Loader, AlertTriangle } from 'lucide-vue-next'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Button } from '@/components/ui/button'

interface Props {
  row: Row<Task>
}

const props = defineProps<Props>()

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
    value: "done", 
    label: "Done", 
    icon: Check, 
    class: "bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100 dark:bg-emerald-500/10 dark:text-emerald-400 dark:border-emerald-500/20 dark:hover:bg-emerald-500/20"
  },
] as const

const currentStatus = ref(props.row.getValue("status") as string | null)
const isOpen = ref(false)
const isUpdating = ref(false)

const currentStyle = computed(() => {
  const statusValue = currentStatus.value
  if (!statusValue) return statuses[0]
  const found = statuses.find(s => s.value === statusValue)
  return found ?? statuses[0]
})

const updateStatus = async (newStatus: string) => {
  if (isUpdating.value || newStatus === currentStatus.value) return
  
  isUpdating.value = true
  
  try {
    const taskId = props.row.original.id
    const response = await fetch(`http://127.0.0.1:4000/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    
    if (!response.ok) throw new Error('Failed to update status')
    
    currentStatus.value = newStatus
    isOpen.value = false
    
    console.log('Status updated successfully')
  } catch (error) {
    console.error('Error updating status:', error)
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <Popover v-model:open="isOpen">
    <PopoverTrigger as-child>
      <Button 
        variant="ghost" 
        :class="`h-7 py-0 px-2.5 rounded-md border text-xs font-medium transition-all ${currentStyle.class}`"
        @click.stop
        :disabled="isUpdating"
      >
        <component 
          :is="currentStyle.icon" 
          class="h-3 w-3 mr-1.5" 
        />
        {{ currentStyle.label }}
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
          :disabled="isUpdating"
          @click="updateStatus(status.value)"
        >
          <component :is="status.icon" class="h-3.5 w-3.5 mr-2" />
          {{ status.label }}
        </Button>
      </div>
    </PopoverContent>
  </Popover>
</template>