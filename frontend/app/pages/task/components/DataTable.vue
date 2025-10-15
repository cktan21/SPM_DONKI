<script setup lang="ts">
import type {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import type { Task } from '../data/schema'

import {
  FlexRender,
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { valueUpdater } from '@/lib/utils'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import DataTablePagination from './DataTablePagination.vue'
import DataTableToolbar from './DataTableToolbar.vue'

interface DataTableProps {
  columns: ColumnDef<Task, any>[]
  data: Task[]
}

const props = defineProps<DataTableProps>()
const router = useRouter()

// Table states
const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])
const columnVisibility = ref<VisibilityState>({})
const rowSelection = ref({})

// Initialize Vue Table
const table = useVueTable({
  get data() {
    return props.data
  },
  get columns() {
    return props.columns
  },
  state: {
    get sorting() {
      return sorting.value
    },
    get columnFilters() {
      return columnFilters.value
    },
    get columnVisibility() {
      return columnVisibility.value
    },
    get rowSelection() {
      return rowSelection.value
    },
  },
  enableRowSelection: true,
  onSortingChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, rowSelection),
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFacetedRowModel: getFacetedRowModel(),
  getFacetedUniqueValues: getFacetedUniqueValues(),
})

// Row click navigation
const handleRowClick = (row: any) => {
  const taskId = row.original.id
  router.push(`/task/${taskId}`)
}
</script>

<template>
  <div class="space-y-4 w-full overflow-hidden">
    <!-- Toolbar -->
    <DataTableToolbar :table="table" />

    <!-- Scrollable table -->
    <div class="w-full overflow-x-auto">
      <div class="inline-block min-w-full align-middle">
        <div class="overflow-hidden rounded-md border border-border">
          <Table class="min-w-full">
            <!-- Header -->
            <TableHeader>
              <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                <TableHead v-for="header in headerGroup.headers" :key="header.id" class="bg-muted/40">
                  <FlexRender v-if="!header.isPlaceholder" :render="header.column.columnDef.header"
                    :props="header.getContext()" />
                </TableHead>
              </TableRow>
            </TableHeader>

            <!-- Body -->
            <TableBody>
              <template v-if="table.getRowModel().rows?.length">
                <TableRow v-for="row in table.getRowModel().rows" :key="row.id"
                  :data-state="row.getIsSelected() && 'selected'"
                  class="cursor-pointer hover:bg-muted/50 transition-colors" @click="() => handleRowClick(row)">
                  <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id" class="whitespace-nowrap">
                    <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                  </TableCell>
                </TableRow>
              </template>

              <!-- Empty state -->
              <TableRow v-else>
                <TableCell :colspan="props.columns.length" class="h-24 text-center text-muted-foreground">
                  No results found.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </div>

    <!-- Small devices: only show selected rows -->
    <div class="block sm:hidden">
      <div class="px-2 text-sm text-muted-foreground">
        {{ table.getFilteredSelectedRowModel().rows.length }} of
        {{ table.getFilteredRowModel().rows.length }} row(s) selected.
      </div>
    </div>

    <!-- Large devices: show full pagination -->
    <div class="hidden sm:block">
      <DataTablePagination :table="table" />
    </div>
  </div>
</template>
