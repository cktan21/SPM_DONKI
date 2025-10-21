<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Row } from '@tanstack/vue-table'
import type { Task } from '../data/schema'
import { Check, Loader, AlertTriangle } from 'lucide-vue-next'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
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
    bgColor: "bg-orange-50", 
    textColor: "text-orange-700", 
    borderColor: "border-orange-200",
    hoverBg: "hover:bg-orange-100"
  },
  { 
    value: "ongoing", 
    label: "Ongoing", 
    icon: AlertTriangle, 
    bgColor: "bg-blue-50", 
    textColor: "text-blue-700", 
    borderColor: "border-blue-200",
    hoverBg: "hover:bg-blue-100"
  },
  { 
    value: "done", 
    label: "Done", 
    icon: Check, 
    bgColor: "bg-emerald-50", 
    textColor: "text-emerald-700", 
    borderColor: "border-emerald-200",
    hoverBg: "hover:bg-emerald-100"
  },
]

const currentStatus = ref(props.row.getValue("status") as string | null)
const isOpen = ref(false)
const isUpdating = ref(false)

const getStatusStyle = (statusValue: string | null) => {
  if (!statusValue) return { 
    bgColor: "bg-gray-50", 
    textColor: "text-gray-600", 
    borderColor: "border-gray-200",
    hoverBg: "hover:bg-gray-100"
  }
  
  const status = statuses.find(s => s.value === statusValue)
  return status || { 
    bgColor: "bg-gray-50", 
    textColor: "text-gray-600", 
    borderColor: "border-gray-200",
    hoverBg: "hover:bg-gray-100"
  }
}

const currentStyle = computed(() => getStatusStyle(currentStatus.value))

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
        :class="`h-5 py-0 px-2 rounded-full border text-xs font-medium ${currentStyle.bgColor} ${currentStyle.textColor} ${currentStyle.borderColor} ${currentStyle.hoverBg} transition-colors`"
        @click.stop
      >
        <component 
          :is="statuses.find(s => s.value === currentStatus)?.icon || Loader" 
          class="h-3 w-3 mr-1" 
        />
        {{ statuses.find(s => s.value === currentStatus)?.label || 'N/A' }}
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-40 p-2" align="start" @click.stop>
      <div class="space-y-1">
        <Button
          v-for="status in statuses"
          :key="status.value"
          variant="ghost"
          size="sm"
          :class="`w-full justify-start text-xs h-8 ${status.value === currentStatus ? 'bg-accent' : ''}`"
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