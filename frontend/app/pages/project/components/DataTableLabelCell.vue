<script setup lang="ts">
import { ref } from 'vue'
import type { Row } from '@tanstack/vue-table'
import type { Task } from '../data/schema'
import { Badge } from '@/components/ui/badge'
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
        class="text-left justify-start px-2 cursor-pointer transition-colors hover:bg-accent hover:text-foreground"
        @click.stop="isOpen = true"
      >
        {{ labels.find(l => l.value === currentLabel)?.label || currentLabel }}
      </Badge>
      <span
        v-else
        class="px-2 py-1 text-xs text-muted-foreground cursor-pointer transition-colors hover:bg-accent"
        @click.stop="isOpen = true"
      >
        Set label
      </span>
    </PopoverTrigger>

    <PopoverContent class="w-48 p-2" align="start" @click.stop>
  <div class="space-y-1">
    <Button
      v-for="label in labels"
      :key="label.value"
      variant="ghost"
      size="sm"
      class="w-full justify-start text-xs h-8 text-left px-0 focus-visible:ring-0 focus:ring-0 focus:outline-none"
      :class="{
        'bg-accent text-foreground': label.value === currentLabel
      }"
      :disabled="isUpdating"
      @click="updateLabel(label.value)"
      tabindex="-1"
    >
      {{ label.label }}
    </Button>
  </div>
</PopoverContent>

  </Popover>
</template>


