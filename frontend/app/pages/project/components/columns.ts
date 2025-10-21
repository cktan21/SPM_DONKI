import type { ColumnDef } from "@tanstack/vue-table"
import type { Task } from "../data/schema"
import type { Component } from "vue"
import { h } from "vue"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import DataTableColumnHeader from "./DataTableColumnHeader.vue"
import DataTableStatusCell from "./DataTableStatusCell.vue"
import DataTableLabelCell from "./DataTableLabelCell.vue"
import { Check, Loader, AlertTriangle } from "lucide-vue-next"

interface StatusOption {
  value: string
  label: string
  icon: Component
}

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'N/A'
  try {
    const formatted = new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
    if (formatted === 'Invalid Date') return 'N/A'
    return formatted
  } catch {
    return 'N/A'
  }
}

export const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

export const statuses: StatusOption[] = [
  { value: "to do", label: "To Do", icon: Loader },
  { value: "ongoing", label: "Ongoing", icon: AlertTriangle },
  { value: "done", label: "Done", icon: Check },
]

export const priorities: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

const truncateId = (id: string | number, maxLength: number = 12): string => {
  const idStr = String(id)
  if (idStr.length <= maxLength) return idStr
  const charsToShow = Math.floor(maxLength / 2) - 1
  return `${idStr.slice(0, charsToShow)}...${idStr.slice(-charsToShow)}`
}

export const columns: ColumnDef<Task>[] = [
  {
    id: "select",
    header: ({ table }) =>
      h(Checkbox, {
        modelValue:
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate"),
        "onUpdate:modelValue": (v) => table.toggleAllPageRowsSelected(!!v),
        ariaLabel: "Select all",
        class: "translate-y-0.5",
      }),
    cell: ({ row }) =>
      h(Checkbox, {
        modelValue: row.getIsSelected(),
        "onUpdate:modelValue": (v) => row.toggleSelected(!!v),
        ariaLabel: "Select row",
        class: "translate-y-0.5",
        onClick: (e: Event) => { e.stopPropagation(); return undefined },
      }),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Task ID" }),
    cell: ({ row }) => {
      const id = row.getValue("id") as string | number
      const fullId = id ? String(id) : "-"
      const displayId = truncateId(fullId, 16)
      return h(TooltipProvider, {}, () => [
        h(Tooltip, {}, () => [
          h(TooltipTrigger, { asChild: true }, () =>
            h("div", { class: "text-center font-mono text-sm cursor-help" }, displayId)
          ),
          h(TooltipContent, { class: "font-mono text-xs" }, () => fullId)
        ])
      ])
    },
    enableSorting: true,
    enableHiding: false,
  },
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
  {
    accessorKey: "label",
    header: ({ column }) =>
      h(
        "div",
        {
          class: "flex justify-start items-center text-left p-0 m-0 w-full",
          style: { padding: "0", margin: "0", width: "100%" }
        },
        h(DataTableColumnHeader, {
          column,
          title: "Label",
          class: "flex justify-start items-center text-left p-0 m-0 w-full"
        })
      ),
    cell: ({ row }) =>
      h(
        "div",
        {
          class: "flex justify-start items-center text-left p-0 m-0 w-full",
          style: { padding: "0", margin: "0", width: "100%" }
        },
        h(DataTableLabelCell, {
          row,
          class: "flex justify-start items-center text-left p-0 m-0 w-full",
          onClick: (e: Event) => {
            e.stopPropagation();
            return undefined;
          },
        })
      ),
    filterFn: (row, id, value) => value.includes(row.getValue(id)),
    enableSorting: false,
    enableHiding: true,
  }


  ,

  {
    accessorKey: "status",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Status" }),
    cell: ({ row }) =>
      h(DataTableStatusCell, {
        row,
        onClick: (e: Event) => { e.stopPropagation(); return undefined }
      }),
    filterFn: (row, id, value) => value.includes(row.getValue(id)),
  },
  {
    accessorKey: "priority",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Priority" }),
    cell: ({ row }) => {
      const priorityValue = row.getValue("priority") as number | null
      let colorClass = ""
      if (priorityValue != null) {
        if (priorityValue >= 7) colorClass = "text-red-600"
        else if (priorityValue >= 4) colorClass = "text-black-500"
        else colorClass = "text-stone-400"
      }
      return h("div", { class: `flex justify-center items-center text-sm font-medium ${colorClass}` },
        priorityValue != null ? String(priorityValue) : "-"
      )
    },
    filterFn: (row, id, value) => Array.isArray(value) ? value.includes(row.getValue(id)) : row.getValue(id) === value,
  },
  {
    accessorKey: "deadline",
    header: ({ column }) => h(DataTableColumnHeader, { column, title: "Deadline" }),
    cell: ({ row }) => {
      const deadlineValue = row.getValue("deadline") as string | null
      return h("div", { class: "text-left text-sm" }, formatDate(deadlineValue))
    },
    enableSorting: true,
    enableHiding: true,
  },
]
