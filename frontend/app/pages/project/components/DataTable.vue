<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { valueUpdater } from '@/lib/utils'
import {
  FlexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  useVueTable,
} from '@tanstack/vue-table'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import SubtaskItem from './SubtaskItem.vue'
import DataTablePagination from './DataTablePagination.vue'
import DataTableToolbar from './DataTableToolbar.vue'

import { ChevronRight } from 'lucide-vue-next'

interface DataTableProps {
  columns: any[]
  data: any[]
}

const props = defineProps<DataTableProps>()
const router = useRouter()

const expandedRows = ref<{ [key: string]: boolean }>({})
const toggleExpand = (id: string) => {
  expandedRows.value[id] = !expandedRows.value[id]
}

const sorting = ref([])
const columnFilters = ref([])
const columnVisibility = ref({})
const rowSelection = ref({})

const table = useVueTable({
  get data() { return props.data },
  get columns() { return props.columns },
  state: {
    get sorting() { return sorting.value },
    get columnFilters() { return columnFilters.value },
    get columnVisibility() { return columnVisibility.value },
    get rowSelection() { return rowSelection.value },
  },
  onSortingChange: (updaterOrValue) => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: (updaterOrValue) => valueUpdater(updaterOrValue, columnFilters),
  onColumnVisibilityChange: (updaterOrValue) => valueUpdater(updaterOrValue, columnVisibility),
  onRowSelectionChange: (updaterOrValue) => valueUpdater(updaterOrValue, rowSelection),
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFacetedRowModel: getFacetedRowModel(),
  getFacetedUniqueValues: getFacetedUniqueValues(),
})

const handleRowClick = (rowId: string, event: Event) => {
  const target = event.target as HTMLElement
  const isActionsColumn = target.closest('[data-actions-cell]')

  if (!isActionsColumn) {
    router.push(`/task/${rowId}`)
  }
}

// Check if a task has subtasks
const hasSubtasks = (row: any) => {
  return row.original.subtasks && row.original.subtasks.length > 0
}
</script>

<template>
  <div class="space-y-4 w-full">
    <DataTableToolbar :table="table" />

    <div class="rounded-md border border-border overflow-auto">
      <Table class="w-full min-w-[800px]">
        <colgroup>
  <col style="width: 50px" />   <!-- Chevron column -->
  <col style="width: 50px" />   <!-- Select checkbox -->
  <col style="width: 140px" />  <!-- Task ID -->
  <col style="width: auto" />   <!-- Name/Title (flexible width) -->
  <col style="width: 120px" />  <!-- Label -->
  <col style="width: 140px" />  <!-- Status -->
  <col style="width: 90px" />   <!-- Priority -->
  <col style="width: 130px" />  <!-- Deadline -->
</colgroup>

        <TableHeader>
          <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <TableHead class="bg-muted/40"></TableHead>
            <TableHead v-for="header in headerGroup.headers" :key="header.id" class="bg-muted/40">
              <FlexRender v-if="!header.isPlaceholder" :render="header.column.columnDef.header"
                :props="header.getContext()" />
            </TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <template v-if="table.getRowModel().rows.length">
            <template v-for="row in table.getRowModel().rows" :key="row.id">
              <TableRow class="hover:bg-muted/50 transition-colors cursor-pointer"
                @click="handleRowClick(row.original.id, $event)">
                <!-- Chevron cell - only show if task has subtasks -->
                <TableCell class="text-center" @click.stop="hasSubtasks(row) ? toggleExpand(row.original.id) : null">
                  <ChevronRight v-if="hasSubtasks(row)" :size="16"
                    class="mx-auto text-muted-foreground transition-transform duration-200 cursor-pointer"
                    :class="expandedRows[row.original.id] ? 'rotate-90 text-foreground' : ''" />
                </TableCell>

                <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id"
                  :data-actions-cell="cell.column.id === 'actions' ? true : undefined" :class="{
                    'max-w-0': cell.column.id === 'title',
                    'min-w-[250px] lg:min-w-0': cell.column.id === 'title',
                    'pl-2': cell.column.id === 'label'
                  }">
                  <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                </TableCell>
              </TableRow>

              <!-- Expanded subtasks row -->
              <tr v-if="expandedRows[row.original.id] && hasSubtasks(row)">
                <td :colspan="row.getVisibleCells().length + 1" class="bg-muted/30 p-4">
                  <div class="space-y-2">
                    <SubtaskItem v-for="sub in row.original.subtasks" :key="sub.id" :subtask="sub"
                      @click="router.push(`/task/${sub.id}`)" />
                  </div>
                </td>
              </tr>
            </template>
          </template>

          <TableRow v-else>
            <TableCell :colspan="props.columns.length + 1" class="h-24 text-center text-muted-foreground">
              No results found.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <div class="hidden sm:block">
      <DataTablePagination :table="table" />
    </div>
  </div>
</template>