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

// ✅ Lucide icon
import { ChevronRight } from 'lucide-vue-next'

interface DataTableProps {
  columns: any[]
  data: any[]
}

const props = defineProps<DataTableProps>()
const router = useRouter()

// Expanded row state
const expandedRows = ref<{ [key: string]: boolean }>({})
const toggleExpand = (id: string) => {
  expandedRows.value[id] = !expandedRows.value[id]
}

// Table states
const sorting = ref([])
const columnFilters = ref([])
const columnVisibility = ref({})
const rowSelection = ref({})

// Initialize Vue Table
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
</script>

<template>
  <div class="space-y-4 w-full overflow-hidden">
    <!-- Toolbar -->
    <DataTableToolbar :table="table" />

    <!-- Table wrapper -->
    <div class="w-full overflow-x-auto">
      <div class="inline-block min-w-full align-middle">
        <div class="overflow-hidden rounded-md border border-border">
          <Table class="min-w-full">
            <!-- Header -->
            <TableHeader>
              <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                <!-- Arrow column header -->
                <TableHead class="w-10 px-2"></TableHead>

                <!-- Regular headers -->
                <TableHead
                  v-for="header in headerGroup.headers"
                  :key="header.id"
                  class="bg-muted/40 px-2 text-left"
                >
                  <FlexRender
                    v-if="!header.isPlaceholder"
                    :render="header.column.columnDef.header"
                    :props="header.getContext()"
                  />
                </TableHead>
              </TableRow>
            </TableHeader>

            <!-- Body -->
            <TableBody>
              <template v-if="table.getRowModel().rows.length">
                <template v-for="row in table.getRowModel().rows" :key="row.id">
                  <!-- Main row -->
                  <TableRow class="cursor-pointer hover:bg-muted/50 transition-colors">
                    <!-- Arrow toggle -->
                    <TableCell
                      class="w-10 text-center px-2"
                      @click.stop="toggleExpand(row.original.id)"
                    >
                      <ChevronRight
                        :size="16"
                        class="mx-auto text-muted-foreground transition-transform duration-200"
                        :class="expandedRows[row.original.id] ? 'rotate-90 text-foreground' : ''"
                      />
                    </TableCell>

                    <!-- Task cells -->
                    <TableCell
                      v-for="cell in row.getVisibleCells()"
                      :key="cell.id"
                      @click="() => router.push(`/task/${row.original.id}`)"
                      class="whitespace-nowrap px-2"
                    >
                      <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                    </TableCell>
                  </TableRow>

                  <!-- Expanded subtasks -->
                  <tr v-if="expandedRows[row.original.id] && row.original.subtasks?.length">
                    <td :colspan="row.getVisibleCells().length + 1" class="bg-muted/30 p-4">
                      <div class="space-y-2">
                        <SubtaskItem
                          v-for="sub in row.original.subtasks"
                          :key="sub.id"
                          :subtask="sub"
                        />
                      </div>
                    </td>
                  </tr>
                </template>
              </template>

              <!-- Empty state -->
              <TableRow v-else>
                <TableCell :colspan="props.columns.length + 1" class="h-24 text-center text-muted-foreground">
                  No results found.
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="hidden sm:block">
      <DataTablePagination :table="table" />
    </div>
  </div>
</template>
