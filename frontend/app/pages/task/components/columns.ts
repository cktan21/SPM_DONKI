import type { ColumnDef } from "@tanstack/vue-table"
import type { Task } from "../data/schema"
import type { Component } from "vue"

import { h } from "vue"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import DataTableColumnHeader from "./DataTableColumnHeader.vue"
import DataTableRowActions from "./DataTableRowActions.vue"

// Import icons
import { Check, Loader, AlertTriangle } from "lucide-vue-next"

// --- Status type ---
interface StatusOption {
  value: string
  label: string
  icon: Component
}

// --- Example static data ---
export const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

export const statuses: StatusOption[] = [
  { value: "todo", label: "To Do", icon: Loader },
  { value: "in_progress", label: "In Progress", icon: AlertTriangle },
  { value: "done", label: "Done", icon: Check },
]

// Priority numbers 1–10
export const priorities: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

// Helper function to truncate ID in the middle
const truncateId = (id: string | number, maxLength: number = 12): string => {
  const idStr = String(id)
  if (idStr.length <= maxLength) return idStr
  
  const charsToShow = Math.floor(maxLength / 2) - 1
  const start = idStr.slice(0, charsToShow)
  const end = idStr.slice(-charsToShow)
  return `${start}...${end}`
}

// --- Columns definition ---
export const columns: ColumnDef<Task>[] = [
  {
    id: "select",
    header: ({ table }) =>
      h(Checkbox, {
        modelValue:
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate"),
        "onUpdate:modelValue": (value) =>
          table.toggleAllPageRowsSelected(!!value),
        ariaLabel: "Select all",
        class: "translate-y-0.5",
      }),
    cell: ({ row }) =>
      h(Checkbox, {
        modelValue: row.getIsSelected(),
        "onUpdate:modelValue": (value) => row.toggleSelected(!!value),
        ariaLabel: "Select row",
        class: "translate-y-0.5",
        onClick: (e: Event) => { e.stopPropagation(); return undefined },
      }),
    enableSorting: false,
    enableHiding: false,
  },

  // Task ID column
  {
    accessorKey: "id",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Task ID" }),
    cell: ({ row }) => {
      const id = row.getValue("id") as string | number
      const fullId = id ? String(id) : "-"
      const displayId = truncateId(fullId, 16)
      
      return h(
        "div",
        { 
          class: "text-center font-mono text-sm",
          title: fullId
        },
        displayId
      )
    },
    enableSorting: true,
    enableHiding: false,
  },

  // Name column
  {
    accessorKey: "title",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Name" }),
    cell: ({ row }) => {
      const label = row.original.label
        ? labels.find((l) => l.value === row.original.label)
        : null
      const title = row.getValue("title") as string | null
      return h("div", { class: "flex items-center gap-2 min-w-0" }, [
        label ? h(Badge, { variant: "outline", class: "shrink-0" }, () => label.label) : null,
        h("span", { class: "truncate font-medium", title: title || undefined }, title || "-"),
      ])
    },
  },

  // Status column
  {
    accessorKey: "status",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Status" }),
    cell: ({ row }) => {
      const statusValue = row.getValue("status") as string | null
      if (!statusValue)
        return h("div", { class: "flex justify-center text-muted-foreground" }, "-")

      const status = statuses.find((s) => s.value === statusValue)
      if (!status) return h("div", { class: "flex justify-center" }, statusValue)

      return h("div", { class: "flex items-center justify-center gap-1" }, [
        h(status.icon, { class: "h-4 w-4 text-muted-foreground shrink-0" }),
        h("span", { class: "text-sm" }, status.label),
      ])
    },
  },

  // Priority column
  {
    accessorKey: "priority",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Priority" }),
    cell: ({ row }) => {
      const priorityValue = row.getValue("priority") as number | null
      return h(
        "div",
        { class: "flex justify-center items-center text-sm font-medium" },
        priorityValue !== null && priorityValue !== undefined ? String(priorityValue) : "-"
      )
    },
  },

  // Actions column
  {
    id: "actions",
    cell: ({ row }) => h(DataTableRowActions, { row }),
  },
]