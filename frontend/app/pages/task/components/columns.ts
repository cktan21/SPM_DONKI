import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import { Badge } from '@/components/ui/badge'

export const columns: ColumnDef<any>[] = [
  {
    accessorKey: 'id',
    header: 'ID',
    cell: ({ row }) => h('div', { class: 'font-mono text-sm text-muted-foreground' }, row.getValue('id')),
  },
  {
    accessorKey: 'title',
    header: 'Title',
    cell: ({ row }) => h('div', { class: 'font-medium' }, row.getValue('title')),
  },
  {
    accessorKey: 'status',
    header: 'Status',
    cell: ({ row }) => {
      const status = row.getValue('status') as string | null
      if (!status) return h('span', { class: 'text-muted-foreground text-sm' }, '—')
      
      // Status badge styling
      const statusStyles: Record<string, string> = {
        'pending': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        'in-progress': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
        'in_progress': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
        'completed': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        'blocked': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
        'cancelled': 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
      }
      
      const statusKey = status.toLowerCase().replace(/\s+/g, '_')
      const badgeClass = statusStyles[statusKey] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
      
      return h(Badge, { 
        variant: 'outline',
        class: `${badgeClass} border-0 capitalize`
      }, () => status.replace(/_/g, ' '))
    },
  },
  {
    accessorKey: 'priority',
    header: 'Priority',
    cell: ({ row }) => {
      const priority = row.getValue('priority') as string | null
      if (!priority) return h('span', { class: 'text-muted-foreground text-sm' }, '—')
      
      // Priority badge styling
      const priorityStyles: Record<string, string> = {
        'critical': 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 font-semibold',
        'high': 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
        'medium': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        'low': 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        'none': 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400',
      }
      
      const priorityKey = priority.toLowerCase()
      const badgeClass = priorityStyles[priorityKey] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
      
      return h(Badge, { 
        variant: 'outline',
        class: `${badgeClass} border-0 capitalize`
      }, () => priority)
    },
  },
]