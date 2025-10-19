<script setup lang="ts">
import { useAttrs, computed } from 'vue'
import type { Column } from '@tanstack/vue-table'
import type { Component } from 'vue'
import type { Task } from '../data/schema'
import { Icon } from '@iconify/vue'

import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList, CommandSeparator } from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Separator } from '@/components/ui/separator'

interface DataTableFacetedFilter {
  column?: Column<Task, any>
  title?: string
  options: {
    label: string
    value: string
    icon?: Component
  }[]
  optionsnumber: number[]
}

const props = defineProps<DataTableFacetedFilter>()

const facets = computed(() => props.column?.getFacetedUniqueValues())
const selectedValues = computed(() => new Set(props.column?.getFilterValue() as (string | number)[]))

// Determine if we're dealing with numbers (priority) or strings (status/label)
const isNumberFilter = computed(() => props.optionsnumber.length > 0)

// Convert number options to the format needed for display
const displayOptions = computed(() => {
  if (isNumberFilter.value) {
    return props.optionsnumber.map(num => ({
      label: String(num),
      value: num, // Keep as number
      icon: undefined, // No icon for numbers
    }))
  }
  return props.options
})

const attrs = useAttrs()
const className = typeof attrs.class === 'string' ? attrs.class : ''
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button variant="outline" size="sm" :class="cn('h-8 border-dashed', className)" v-bind="attrs">
        <Icon icon="radix-icons:plus-circled" class="mr-2 h-4 w-4" />
        {{ title }}
        <template v-if="selectedValues.size > 0">
          <Separator orientation="vertical" class="mx-2 h-4" />
          <Badge
            variant="secondary"
            class="rounded-sm px-1 font-normal lg:hidden"
          >
            {{ selectedValues.size }}
          </Badge>
          <div class="hidden space-x-1 lg:flex">
            <Badge
              v-if="selectedValues.size > 2"
              variant="secondary"
              class="rounded-sm px-1 font-normal"
            >
              {{ selectedValues.size }} selected
            </Badge>
            <template v-else>
              <Badge
                v-for="option in displayOptions
                  .filter((option) => selectedValues.has(option.value))"
                :key="option.value"
                variant="secondary"
                class="rounded-sm px-1 font-normal"
              >
                {{ option.label }}
              </Badge>
            </template>
          </div>
        </template>
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0" align="start">
      <Command>
        <CommandInput :placeholder="title" />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          <CommandGroup>
            <CommandItem
              v-for="option in displayOptions"
              :key="option.value"
              :value="option"
              @select="(e) => {
                const optionValue = option.value
                const isSelected = selectedValues.has(optionValue)
                
                if (isSelected) {
                  selectedValues.delete(optionValue)
                } else {
                  selectedValues.add(optionValue)
                }
                
                const filterValues = Array.from(selectedValues)
                column?.setFilterValue(filterValues.length ? filterValues : undefined)
              }"
            >
              <div
                :class="cn(
                  'mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary',
                  selectedValues.has(option.value)
                    ? 'bg-primary text-primary-foreground'
                    : 'opacity-50 [&_svg]:invisible',
                )"
              >
                <Icon icon="radix-icons:check" :class="cn('h-4 w-4')" />
              </div>

              <component :is="option.icon" v-if="option.icon" class="mr-2 h-4 w-4 text-muted-foreground" />
              <span>{{ option.label }}</span>
              <span v-if="facets?.get(option.value)" class="ml-auto flex h-4 w-4 items-center justify-center font-mono text-xs">
                {{ facets.get(option.value) }}
              </span>
            </CommandItem>
          </CommandGroup>
          <template v-if="selectedValues.size > 0">
            <CommandSeparator />
            <CommandGroup>
              <CommandItem
                :value="{ label: 'Clear filters' }"
                class="justify-center text-center"
                @select="column?.setFilterValue(undefined)"
              >
                Clear filters
              </CommandItem>
            </CommandGroup>
          </template>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>