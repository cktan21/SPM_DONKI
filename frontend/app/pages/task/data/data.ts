import { h } from 'vue'
import { Icon } from '@iconify/vue'

export const labels = [
  { value: 'bug', label: 'Bug' },
  { value: 'feature', label: 'Feature' },
  { value: 'documentation', label: 'Documentation' },
]

const iconify = (name: string, className = 'h-4 w-4') => h(Icon, { icon: name, class: className })

export const statuses = [
  { value: 'backlog', label: 'Backlog', icon: iconify('radix-icons:question-mark-circled') },
  { value: 'todo', label: 'Todo', icon: iconify('radix-icons:circle') },
  { value: 'in progress', label: 'In Progress', icon: iconify('radix-icons:stopwatch') },
  { value: 'done', label: 'Done', icon: iconify('radix-icons:check-circled') },
  { value: 'canceled', label: 'Canceled', icon: iconify('radix-icons:cross-circled') },
]

export const priorities = [
  { value: 1, label: 1, icon: iconify('radix-icons:arrow-down') },
  { value: 2, label: 2, icon: iconify('radix-icons:arrow-down') },
  { value: 3, label: 3, icon: iconify('radix-icons:arrow-down') },
  { value: 4, label: 4, icon: iconify('radix-icons:arrow-down') },
  { value: 5, label: 5, icon: iconify('radix-icons:arrow-down') },
  { value: 6, label: 6, icon: iconify('radix-icons:arrow-down') },
  { value: 7, label: 7, icon: iconify('radix-icons:arrow-down') },
  { value: 8, label: 8, icon: iconify('radix-icons:arrow-down') },
  { value: 9, label: 9, icon: iconify('radix-icons:arrow-down') },
  { value: 10, label: 10, icon: iconify('radix-icons:arrow-down') },
]