<script setup lang="ts">
import { ref } from 'vue'
import type { Row } from '@tanstack/vue-table'
import type { Task } from '../data/schema'
import { Badge } from '@/components/ui/badge'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Button } from '@/components/ui/button'

interface Props {
  row: Row<Task>
}

const props = defineProps<Props>()

const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

const currentLabel = ref(props.row.getValue("label") as string | null)
const isOpen = ref(false)
const isUpdating = ref(false)

const updateLabel = async (newLabel: string) => {
  if (isUpdating.value || newLabel === currentLabel.value) return
  
  isUpdating.value = true
  
  try {
    const taskId = props.row.original.id
    const response = await fetch(`http://127.0.0.1:4000/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ label: newLabel })
    })
    
    if (!response.ok) throw new Error('Failed to update label')
    
    currentLabel.value = newLabel
    isOpen.value = false
    
    console.log('Label updated successfully')
  } catch (error) {
    console.error('Error updating label:', error)
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <Popover v-model:open="isOpen">
    <PopoverTrigger as-child>
      <Badge
        v-if="currentLabel"
        variant="outline"
        class="capitalize px-2.5 py-1 text-xs font-medium cursor-pointer transition-all hover:shadow-sm bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100 dark:bg-purple-500/10 dark:text-purple-400 dark:border-purple-500/20 dark:hover:bg-purple-500/20"
        @click.stop="isOpen = true"
      >
        {{ labels.find(l => l.value === currentLabel)?.label || currentLabel }}
      </Badge>
      <Button
        v-else
        variant="ghost"
        size="sm"
        class="h-7 px-2.5 text-xs text-slate-500 hover:text-slate-700 hover:bg-slate-50 dark:text-slate-400 dark:hover:text-slate-300 dark:hover:bg-slate-800"
        @click.stop="isOpen = true"
      >
        Set label
      </Button>
    </PopoverTrigger>

    <PopoverContent class="w-48 p-1.5 shadow-lg border-slate-200 dark:border-slate-800" align="start" @click.stop>
      <div class="space-y-0.5">
        <Button
          v-for="label in labels"
          :key="label.value"
          variant="ghost"
          size="sm"
          class="w-full justify-start text-xs h-8 rounded-md"
          :class="{
            'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100': label.value === currentLabel,
            'hover:bg-slate-50 dark:hover:bg-slate-900': label.value !== currentLabel
          }"
          :disabled="isUpdating"
          @click="updateLabel(label.value)"
        >
          {{ label.label }}
        </Button>
      </div>
    </PopoverContent>
  </Popover>
</template>