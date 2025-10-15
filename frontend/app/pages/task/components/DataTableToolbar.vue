<script setup lang="ts">
import type { Table } from '@tanstack/vue-table'
import type { Task } from '../data/schema'
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { priorities, statuses } from '../data/data'
import DataTableFacetedFilter from './DataTableFacetedFilter.vue'
import DataTableViewOptions from './DataTableViewOptions.vue'

interface DataTableToolbarProps {
  table: Table<Task>
}

const props = defineProps<DataTableToolbarProps>()

const isFiltered = computed(() => props.table.getState().columnFilters.length > 0)
</script>

<template>
  <div class="flex flex-col gap-3">
    <!-- First row: Search input (full width on mobile) -->
    <div class="w-full">
      <Input
        placeholder="Filter tasks..."
        :model-value="(table.getColumn('title')?.getFilterValue() as string) ?? ''"
        class="h-8 w-full"
        @input="table.getColumn('title')?.setFilterValue($event.target.value)"
      />
    </div>

    <!-- Second row: Filters and view options -->
    <div class="flex flex-col sm:flex-row gap-2 sm:items-center sm:justify-between">
      <!-- Left side: Status, Priority filters and Reset button -->
      <div class="flex gap-2 flex-1">
        <DataTableFacetedFilter
          v-if="table.getColumn('status')"
          :column="table.getColumn('status')"
          title="Status"
          :options="statuses"
          :optionsnumber="[]"
          class="flex-1 sm:flex-none"
        />
        <DataTableFacetedFilter
          v-if="table.getColumn('priority')"
          :column="table.getColumn('priority')"
          title="Priority"
          :options="[]"
          :optionsnumber="priorities"
          class="flex-1 sm:flex-none"
        />
        <Button
          v-if="isFiltered"
          variant="ghost"
          class="h-8 px-2 lg:px-3 flex-1 sm:flex-none"
          @click="table.resetColumnFilters()"
        >
          Reset
          <Icon icon="radix-icons:cross-2" class="ml-2 h-4 w-4" />
        </Button>
      </div>

      <!-- Right side: View options (hidden on mobile) -->
      <div class="hidden sm:block shrink-0">
        <DataTableViewOptions :table="table" />
      </div>
    </div>
  </div>
</template>