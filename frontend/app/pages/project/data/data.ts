import { z } from 'zod'
import type { Component } from "vue"
import { Check, Loader, AlertTriangle } from "lucide-vue-next"

// Schema matching your API structure with all fields
export const taskSchema = z.object({
  id: z.string(),
  name: z.string(),
  desc: z.string().nullable().optional(),
  notes: z.string().nullable().optional(),
  priorityLevel: z.number(),
  priorityLabel: z.string(),
  created_by_uid: z.string(),
  updated_timestamp: z.string(),
  parentTaskId: z.string().nullable().optional(),
  collaborators: z.array(z.string()).nullable().optional(),
  pid: z.string(),
  // Derived/mapped fields for table display
  title: z.string().optional(), // Mapped from 'name'
  status: z.string().nullable().optional(), // Can be null if not provided
  label: z.string().nullable().optional(), // Can be null if not provided
  priority: z.number().optional(), // Mapped from 'priorityLevel'
})

export type Task = z.infer<typeof taskSchema>



export const labels = [
  { value: "bug", label: "Bug" },
  { value: "feature", label: "Feature" },
  { value: "documentation", label: "Documentation" },
]

export const priorities: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

export const statuses = [
  { value: "todo", label: "To Do", icon: Loader },
  { value: "ongoing", label: "Ongoing", icon: AlertTriangle },
  { value: "done", label: "Done", icon: Check },
]