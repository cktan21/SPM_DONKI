export const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', { month: 'short', day: 'numeric', year: 'numeric' })
}

export const formatDateShort = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' })
}

export const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
}

export const getStatusColor = (status) => {
  const colors = {
    'to do': 'bg-slate-400',
    'ongoing': 'bg-blue-500',
    'done': 'bg-green-500',
    'overdue': 'bg-red-500'
  }
  return colors[status] || 'bg-slate-400'
}

export const getStatusBadgeClass = (status) => {
  const classes = {
    'to do': 'bg-slate-100 text-slate-700',
    'ongoing': 'bg-blue-50 text-blue-700',
    'done': 'bg-green-50 text-green-700',
    'overdue': 'bg-red-50 text-red-700'
  }
  return classes[status] || 'bg-slate-100 text-slate-700'
}

export const getPriorityColor = (level) => {
  if (level >= 8) return 'bg-red-100 text-red-700'
  if (level >= 4) return 'bg-yellow-100 text-yellow-700'
  return 'bg-green-100 text-green-700'
}