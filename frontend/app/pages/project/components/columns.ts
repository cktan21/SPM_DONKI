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

// Helper to format date
const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    const formatted = new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
    if (formatted === 'Invalid Date') {
      return 'N/A'
    }
    return formatted
  } catch {
    return 'N/A'
  }
}

// --- Example static data ---
export const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

export const statuses: StatusOption[] = [
  { value: "todo", label: "To Do", icon: Loader },
  { value: "ongoing", label: "Ongoing", icon: AlertTriangle },
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

  // Name column - will take remaining space
  {
    accessorKey: "title",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Name" }),
    cell: ({ row }) => {
      const title = row.getValue("title") as string | null
      return h("div", { class: "flex items-center gap-2 min-w-0" }, [
        h("span", { class: "truncate font-medium", title: title || undefined }, title || "-"),
      ])
    },
  },

  

  // Label column (hidden but used for filtering)
  {
    accessorKey: "label",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Label" }),
    cell: ({ row }) => {
      const labelValue = row.getValue("label") as string | null
      if (!labelValue) return null

      const label = labels.find((l) => l.value === labelValue)
      return label ? h(Badge, { variant: "outline" }, () => label.label) : null
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
    enableSorting: false,
    enableHiding: true,
  },

  // Status column
  {
    accessorKey: "status",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Status" }),
    cell: ({ row }) => {
      const statusValue = row.getValue("status") as string | null
      console.log("Status value:", statusValue)

      if (!statusValue)
        return h(
          "div",
          { class: "flex justify-center text-muted-foreground" },
          "-"
        )

      console.log("raw statusValue:", JSON.stringify(statusValue))
      console.log("statusValue chars:", Array.from(String(statusValue)).map(c => c.charCodeAt(0)))
      console.log("available status values:", statuses.map(s => s.value))
      const status = statuses.find((s) => s.value === statusValue)
      if (!status)
        return h("div", { class: "flex justify-center" }, statusValue)
      console.log("Status value:", statusValue)


      // 🎨 Color mapping based on status
      let colorClass = ""
      switch (statusValue.toLowerCase()) {
        case "done":
          colorClass = "text-green-500"
          break
        case "ongoing":
        case "in_progress":
          colorClass = "text-blue-500"
          break
        case "todo":
          colorClass = "text-orange-500"
          break
        default:
          colorClass = "text-muted-foreground"
      }

      return h("div", { class: "flex items-center justify-center gap-1" }, [
        h(status.icon, { class: `h-4 w-4 ${colorClass} shrink-0` }),
        h("span", { class: `text-sm font-medium ${colorClass}` }, status.label),
      ])
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },


  // Priority column
  {
    accessorKey: "priority",
    header: ({ column }) =>
      h(DataTableColumnHeader, { column, title: "Priority" }),
    cell: ({ row }) => {
      const priorityValue = row.getValue("priority") as number | null

      // Determine color based on priority range
      let colorClass = ""
      if (priorityValue !== null && priorityValue !== undefined) {
        if (priorityValue >= 7) colorClass = "text-red-600"
        else if (priorityValue >= 4) colorClass = "text-black-500"
        else colorClass = "text-stone-400"
      }

      return h(
        "div",
        {
          class: `flex justify-center items-center text-sm font-medium ${colorClass}`,
        },
        priorityValue !== null && priorityValue !== undefined
          ? String(priorityValue)
          : "-"
      )
    },
    filterFn: (row, id, value) => {
      const rowValue = row.getValue(id)
      if (Array.isArray(value)) {
        return value.includes(rowValue)
      }
      return rowValue === value
    },
  },


    // Deadline column (NEW)
  {
    accessorKey: "deadline",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Deadline" }),
    cell: ({ row }) => {
      const deadlineValue = row.getValue("deadline") as string | null
      return h(
        "div",
        { class: "text-center text-sm" },
        formatDate(deadlineValue)
      )
    },
    enableSorting: true,
    enableHiding: true,
  },

  // Actions column
  {
    id: "actions",
    cell: ({ row }) => h(DataTableRowActions, { row }),
  },
]