<script setup lang="ts">

definePageMeta({
  ssr: false
})

import { ref, computed, onMounted, watch } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Skeleton } from '@/components/ui/skeleton'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Checkbox } from '@/components/ui/checkbox'
import { FileText, Download, Filter, BarChart3, Users, FolderKanban, Calendar, TrendingUp, AlertCircle, ChevronDown, X } from 'lucide-vue-next'

let jsPDF: any
let autoTable: any
let XLSX: any

onMounted(async () => {
  const jsPDFModule = await import('jspdf')
  const autoTableModule = await import('jspdf-autotable')
  const xlsxModule = await import('xlsx')

  jsPDF = jsPDFModule.default
  autoTable = autoTableModule.default
  XLSX = xlsxModule
})

// Types
interface User {
  id: string
  name: string
  email?: string
  role?: string
}

interface Task {
  id: string
  name: string
  status: string
  deadline: string
  created_by: User
  collaborators: User[]
  priorityLevel: number
  label: string
  desc?: string
  project: {
    id: string
    name: string
  }
}

interface Project {
  id: string
  name: string
  desc: string
  members: string[]
  tasks: Task[]
}

interface ApiResponse {
  user_id: string
  user_name: string
  user_role: string
  user_dept: string
  projects: Project[]
}

interface ReportData {
  id: string
  filterType: 'user' | 'project' | 'team'
  filterId: string
  filterName: string
  timestamp: string
  timePeriod?: 'week' | 'month'
  periodStart?: string
  periodEnd?: string
  stats: {
    completed: number
    inProgress: number
    todo: number
    overdue: number
    total: number
  }
  tasks: Task[]
}

// State
const loading = ref(true)
const error = ref<string | null>(null)
const data = ref<ApiResponse | null>(null)

const filterType = ref<string>('project')
const selectedFilter = ref<string>('')
const selectedUsers = ref<string[]>([])
const timePeriod = ref<string>('week')
const currentReport = ref<ReportData | null>(null)
const generating = ref(false)
const isUserSelectOpen = ref(false)

// User data from middleware
const userData = useState<{ user: User }>('userData')
const user = computed(() => userData.value?.user)

// Check if user can generate team reports
const canGenerateTeamReports = computed(() => {
  const userRole = data.value?.user_role?.toLowerCase()
  return userRole === 'manager' || userRole === 'hr' || userRole === 'admin'
})

// Computed
const projects = computed(() => data.value?.projects || [])

const users = computed(() => {
  if (!data.value) return []

  const userMap = new Map<string, User>()

  data.value.projects.forEach((project) => {
    project.tasks.forEach((task) => {
      userMap.set(task.created_by.id, task.created_by)
      task.collaborators.forEach((collab) => {
        userMap.set(collab.id, collab)
      })
    })
  })

  return Array.from(userMap.values())
})

// Get unique teams (departments) from projects
const teams = computed(() => {
  if (!data.value) return []
  
  const teamSet = new Set<string>()
  data.value.projects.forEach((project) => {
    project.tasks.forEach((task) => {
      if (task.created_by.role) {
        teamSet.add(task.created_by.role)
      }
      task.collaborators.forEach((collab) => {
        if (collab.role) {
          teamSet.add(collab.role)
        }
      })
    })
  })
  
  return Array.from(teamSet).map(team => ({
    id: team.toLowerCase().replace(/\s+/g, '-'),
    name: team
  }))
})

const selectedUsersDisplay = computed(() => {
  if (selectedUsers.value.length === 0) return 'Select users'
  if (selectedUsers.value.length === 1) {
    return users.value.find(u => u.id === selectedUsers.value[0])?.name || 'Select users'
  }
  return `${selectedUsers.value.length} users selected`
})

const statsCards = computed(() => {
  if (!currentReport.value) return []

  return [
    { label: 'Completed', value: currentReport.value.stats.completed, color: 'bg-green-500', icon: '✓' },
    { label: 'In Progress', value: currentReport.value.stats.inProgress, color: 'bg-blue-500', icon: '●' },
    { label: 'To Do', value: currentReport.value.stats.todo, color: 'bg-gray-500', icon: '○' },
    { label: 'Overdue', value: currentReport.value.stats.overdue, color: 'bg-red-500', icon: '!' },
  ]
})

// Helper to get date range for week/month
const getDateRange = (period: string) => {
  const now = new Date()
  const end = new Date(now)
  let start = new Date(now)
  
  if (period === 'week') {
    // Get start of current week (Sunday)
    start.setDate(now.getDate() - now.getDay())
    start.setHours(0, 0, 0, 0)
  } else {
    // Get start of current month
    start = new Date(now.getFullYear(), now.getMonth(), 1)
  }
  
  return { start, end }
}

// Methods
const fetchData = async () => {
  try {
    loading.value = true

    if (!user.value?.id) {
      throw new Error('User not authenticated')
    }

    const response = await $fetch<ApiResponse>(`http://127.0.0.1:4100/uid/${user.value.id}`, {
      method: 'GET',
      credentials: 'include',
    })

    data.value = response

    // Load saved report from sessionStorage
    const savedReport = sessionStorage.getItem('currentReport')
    if (savedReport) {
      currentReport.value = JSON.parse(savedReport)
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred'
  } finally {
    loading.value = false
  }
}

const generateReportId = () => {
  return Math.random().toString(36).substring(2, 10).toUpperCase()
}

const calculateStats = (tasks: Task[], filterByDate: boolean = false, dateRange?: { start: Date, end: Date }) => {
  const now = new Date()
  let filteredTasks = tasks
  
  // Filter by date range if team report
  if (filterByDate && dateRange) {
    filteredTasks = tasks.filter(task => {
      const taskDate = new Date(task.deadline)
      return taskDate >= dateRange.start && taskDate <= dateRange.end
    })
  }
  
  const stats = {
    completed: 0,
    inProgress: 0,
    todo: 0,
    overdue: 0,
    total: filteredTasks.length,
  }

  filteredTasks.forEach((task) => {
    const deadline = new Date(task.deadline)
    const status = task.status.toLowerCase()

    if (status === 'done') {
      stats.completed++
    } else if (status === 'ongoing') {
      stats.inProgress++
    } else if (status === 'to do') {
      stats.todo++
    } else if (status === 'overdue' || (deadline < now && status !== 'done')) {
      stats.overdue++
    }
  })

  return { stats, tasks: filteredTasks }
}

const handleFilterTypeChange = () => {
  selectedFilter.value = ''
  selectedUsers.value = []
}

const toggleUserSelection = (userId: string) => {
  const index = selectedUsers.value.indexOf(userId)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  } else {
    selectedUsers.value.push(userId)
  }
}

const removeUser = (userId: string) => {
  const index = selectedUsers.value.indexOf(userId)
  if (index > -1) {
    selectedUsers.value.splice(index, 1)
  }
}

const isUserSelected = (userId: string) => {
  return selectedUsers.value.includes(userId)
}

const handleGenerateReport = () => {
  if (!data.value) return
  
  // Check if filter is selected
  if (filterType.value === 'team' && selectedUsers.value.length === 0) return
  if (filterType.value !== 'team' && !selectedFilter.value) return

  generating.value = true
  setTimeout(() => {
    let tasks: Task[] = []
    let filterName = ''
    let dateRange: { start: Date, end: Date } | undefined

    if (filterType.value === 'team') {
      // Get date range for team reports
      dateRange = getDateRange(timePeriod.value)
      
      // Get all tasks from all projects
      const allTasks = data.value!.projects.flatMap((p) => p.tasks)
      
      // Filter by selected users
      tasks = allTasks.filter((task) =>
        selectedUsers.value.includes(task.created_by.id) ||
        task.collaborators.some((c) => selectedUsers.value.includes(c.id))
      )
      
      const selectedUserNames = selectedUsers.value
        .map(id => users.value.find(u => u.id === id)?.name)
        .filter(Boolean)
      
      filterName = `${selectedUserNames.join(', ')} (${timePeriod.value === 'week' ? 'This Week' : 'This Month'})`
    } else if (filterType.value === 'project') {
      const project = data.value!.projects.find((p) => p.id === selectedFilter.value)
      if (project) {
        tasks = project.tasks
        filterName = project.name
      }
    } else {
      const allTasks = data.value!.projects.flatMap((p) => p.tasks)
      tasks = allTasks.filter((task) =>
        task.created_by.id === selectedFilter.value ||
        task.collaborators.some((c) => c.id === selectedFilter.value)
      )

      const foundUser = users.value.find((u) => u.id === selectedFilter.value)
      filterName = foundUser?.name || 'Unknown User'
    }

    // Calculate stats with optional date filtering
    const { stats, tasks: filteredTasks } = calculateStats(
      tasks, 
      filterType.value === 'team',
      dateRange
    )

    const report: ReportData = {
      id: generateReportId(),
      filterType: filterType.value as 'user' | 'project' | 'team',
      filterId: filterType.value === 'team' ? selectedUsers.value.join(',') : selectedFilter.value,
      filterName,
      timestamp: new Date().toISOString(),
      ...(filterType.value === 'team' && {
        timePeriod: timePeriod.value as 'week' | 'month',
        periodStart: dateRange?.start.toISOString(),
        periodEnd: dateRange?.end.toISOString(),
      }),
      stats,
      tasks: filteredTasks,
    }

    currentReport.value = report
    generating.value = false
  }, 800)
}

const exportToPDF = () => {
  if (!process.client || !currentReport.value || !jsPDF || !autoTable) return
  const doc = new jsPDF()

  // Header
  doc.setFontSize(20)
  doc.setTextColor(31, 41, 55)
  doc.text('Task Completion Report', 14, 20)

  doc.setFontSize(10)
  doc.setTextColor(107, 114, 128)
  doc.text(`Report ID: ${currentReport.value.id}`, 14, 28)
  doc.text(`Generated: ${new Date(currentReport.value.timestamp).toLocaleString()}`, 14, 34)
  
  let yPos = 40
  if (currentReport.value.filterType === 'team') {
    doc.text(`Filter: Team Summary - ${currentReport.value.filterName}`, 14, yPos)
    yPos += 6
    doc.text(`Period: ${new Date(currentReport.value.periodStart!).toLocaleDateString()} - ${new Date(currentReport.value.periodEnd!).toLocaleDateString()}`, 14, yPos)
  } else {
    doc.text(`Filter: ${currentReport.value.filterType === 'user' ? 'By User' : 'By Project'} - ${currentReport.value.filterName}`, 14, yPos)
  }

  // Summary Stats
  doc.setFontSize(14)
  doc.setTextColor(31, 41, 55)
  doc.text('Summary', 14, yPos + 12)

  const summaryData: (string | number)[][] = [
    ['Metric', 'Count', 'Percentage'],
    ['Completed', currentReport.value.stats.completed.toString(), `${Math.round((currentReport.value.stats.completed / currentReport.value.stats.total) * 100)}%`],
    ['In Progress', currentReport.value.stats.inProgress.toString(), `${Math.round((currentReport.value.stats.inProgress / currentReport.value.stats.total) * 100)}%`],
    ['To Do', currentReport.value.stats.todo.toString(), `${Math.round((currentReport.value.stats.todo / currentReport.value.stats.total) * 100)}%`],
    ['Overdue', currentReport.value.stats.overdue.toString(), `${Math.round((currentReport.value.stats.overdue / currentReport.value.stats.total) * 100)}%`],
    ['Total Tasks', currentReport.value.stats.total.toString(), '100%'],
  ]

  autoTable(doc, {
    startY: yPos + 16,
    head: [summaryData[0]],
    body: summaryData.slice(1),
    theme: 'grid',
    headStyles: { fillColor: [59, 130, 246] },
  })

  // Task Details
  const finalY = (doc as any).lastAutoTable.finalY || yPos + 16
  doc.setFontSize(14)
  doc.text('Task Details', 14, finalY + 10)

  // Build task data
  let taskHeaders: string[]
  let taskData: (string | number)[][]

  if (currentReport.value.filterType === 'user' || currentReport.value.filterType === 'team') {
    taskHeaders = ['Project', 'Task Name', 'Status', 'Priority', 'Deadline', 'Assigned To']
    taskData = currentReport.value.tasks.map((task) => [
      task.project.name,
      task.name,
      task.status,
      task.priorityLevel.toString(),
      new Date(task.deadline).toLocaleDateString(),
      task.collaborators.map((c) => c.name).join(', ') || 'None',
    ])
  } else {
    taskHeaders = ['Task Name', 'Status', 'Priority', 'Deadline', 'Assigned To']
    taskData = currentReport.value.tasks.map((task) => [
      task.name,
      task.status,
      task.priorityLevel.toString(),
      new Date(task.deadline).toLocaleDateString(),
      task.collaborators.map((c) => c.name).join(', ') || 'None',
    ])
  }

  autoTable(doc, {
    startY: finalY + 14,
    head: [taskHeaders],
    body: taskData,
    theme: 'striped',
    headStyles: { fillColor: [59, 130, 246] },
  })

  doc.save(`report-${currentReport.value.id}.pdf`)
}

const exportToExcel = () => {
  if (!process.client || !currentReport.value || !XLSX) return
  const wb = XLSX.utils.book_new()

  // Summary sheet
  const summaryData: (string | number)[][] = [
    ['Task Completion Report'],
    ['Report ID', currentReport.value.id],
    ['Generated', new Date(currentReport.value.timestamp).toLocaleString()],
    ['Filter Type', currentReport.value.filterType === 'user' ? 'By User' : currentReport.value.filterType === 'team' ? 'Team Summary' : 'By Project'],
    ['Filter Name', currentReport.value.filterName],
  ]

  if (currentReport.value.filterType === 'team') {
    summaryData.push(
      ['Time Period', currentReport.value.timePeriod === 'week' ? 'Weekly' : 'Monthly'],
      ['Period Start', new Date(currentReport.value.periodStart!).toLocaleDateString()],
      ['Period End', new Date(currentReport.value.periodEnd!).toLocaleDateString()]
    )
  }

  summaryData.push(
    [],
    ['Summary Statistics'],
    ['Metric', 'Count', 'Percentage'],
    ['Completed', currentReport.value.stats.completed, `${Math.round((currentReport.value.stats.completed / currentReport.value.stats.total) * 100)}%`],
    ['In Progress', currentReport.value.stats.inProgress, `${Math.round((currentReport.value.stats.inProgress / currentReport.value.stats.total) * 100)}%`],
    ['To Do', currentReport.value.stats.todo, `${Math.round((currentReport.value.stats.todo / currentReport.value.stats.total) * 100)}%`],
    ['Overdue', currentReport.value.stats.overdue, `${Math.round((currentReport.value.stats.overdue / currentReport.value.stats.total) * 100)}%`],
    ['Total Tasks', currentReport.value.stats.total, '100%']
  )

  const summarySheet = XLSX.utils.aoa_to_sheet(summaryData)
  XLSX.utils.book_append_sheet(wb, summarySheet, 'Summary')

  // Tasks sheet
  let taskData: (string | number)[][]

  if (currentReport.value.filterType === 'user' || currentReport.value.filterType === 'team') {
    taskData = [
      ['Project', 'Task Name', 'Status', 'Priority', 'Deadline', 'Assigned To', 'Created By', 'Description'],
      ...currentReport.value.tasks.map((task) => [
        task.project.name,
        task.name,
        task.status,
        task.priorityLevel,
        new Date(task.deadline).toLocaleDateString(),
        task.collaborators.map((c) => c.name).join(', '),
        task.created_by.name,
        task.desc || '',
      ]),
    ]
  } else {
    taskData = [
      ['Task Name', 'Status', 'Priority', 'Deadline', 'Assigned To', 'Created By', 'Description'],
      ...currentReport.value.tasks.map((task) => [
        task.name,
        task.status,
        task.priorityLevel,
        new Date(task.deadline).toLocaleDateString(),
        task.collaborators.map((c) => c.name).join(', '),
        task.created_by.name,
        task.desc || '',
      ]),
    ]
  }

  const taskSheet = XLSX.utils.aoa_to_sheet(taskData)
  XLSX.utils.book_append_sheet(wb, taskSheet, 'Tasks')

  XLSX.writeFile(wb, `report-${currentReport.value.id}.xlsx`)
}

const getStatusBadge = (status: string) => {
  const statusLower = status.toLowerCase()
  const variants: Record<string, string> = {
    'done': 'bg-emerald-50 text-emerald-700 border-emerald-200',
    'ongoing': 'bg-blue-50 text-blue-700 border-blue-200',
    'to do': 'bg-orange-50 text-orange-700 border-orange-200',
    'overdue': 'bg-red-50 text-red-700 border-red-200',
  }
  return variants[statusLower] || variants['to do']
}

const getPriorityColor = (priority: number) => {
  return 'text-gray-900'
}

const getPercentage = (value: number) => {
  if (!currentReport.value) return '0%'
  const total = currentReport.value.stats.total
  return total > 0 ? `${Math.round((value / total) * 100)}%` : '0%'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const formatDeadline = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Watchers
watch(currentReport, (newReport) => {
  if (newReport) {
    sessionStorage.setItem('currentReport', JSON.stringify(newReport))
  }
}, { deep: true })

// Lifecycle
onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 tracking-tight">Report Generator</h1>
          <p class="text-gray-600 mt-2">Generate comprehensive task completion reports</p>
        </div>
        <div class="flex items-center gap-2">
          <BarChart3 class="w-8 h-8 text-blue-500" />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-6">
        <Skeleton class="h-12 w-64" />
        <Skeleton class="h-96 w-full" />
      </div>

      <!-- Error State -->
      <Alert v-else-if="error" variant="destructive">
        <AlertCircle class="h-4 w-4" />
        <AlertDescription>{{ error }}</AlertDescription>
      </Alert>

      <!-- Main Content -->
      <template v-else>
        <!-- Filter Section -->
        <Card class="border-0 shadow-lg bg-white">
          <CardHeader>
            <div class="flex items-center gap-2">
              <Filter class="w-5 h-5 text-blue-500" />
              <CardTitle>Report Filters</CardTitle>
            </div>
            <CardDescription>Select criteria to generate your report</CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- Filter Type -->
              <div class="space-y-2">
                <label class="text-sm font-medium text-gray-700 flex items-center gap-2">
                  <TrendingUp class="w-4 h-4" />
                  Filter By
                </label>
                <Select v-model="filterType" @update:modelValue="handleFilterTypeChange">
                  <SelectTrigger class="h-11">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="project">
                      <div class="flex items-center gap-2">
                        <FolderKanban class="w-4 h-4" />
                        Project
                      </div>
                    </SelectItem>
                    <SelectItem value="user">
                      <div class="flex items-center gap-2">
                        <Users class="w-4 h-4" />
                        User
                      </div>
                    </SelectItem>
                    <SelectItem value="team" v-if="canGenerateTeamReports">
                      <div class="flex items-center gap-2">
                        <Users class="w-4 h-4" />
                        Team Summary
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <!-- Filter Selection -->
              <div class="space-y-2">
                <label class="text-sm font-medium text-gray-700 flex items-center gap-2">
                  <component :is="filterType === 'project' ? FolderKanban : Users" class="w-4 h-4" />
                  Select {{ filterType === 'project' ? 'Project' : filterType === 'team' ? 'Users' : 'User' }}
                </label>
                
                <!-- Multi-select for Team -->
                <Popover v-if="filterType === 'team'" v-model:open="isUserSelectOpen">
                  <PopoverTrigger as-child>
                    <Button
                      variant="outline"
                      role="combobox"
                      class="w-full h-11 justify-between font-normal"
                    >
                      <span class="truncate">{{ selectedUsersDisplay }}</span>
                      <ChevronDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent class="w-full p-0" align="start">
                    <div class="max-h-64 overflow-y-auto p-2">
                      <div v-for="user in users" :key="user.id" 
                        class="flex items-center space-x-2 rounded-sm px-2 py-2 hover:bg-gray-100 cursor-pointer"
                        @click="toggleUserSelection(user.id)">
                        <Checkbox 
                          :checked="isUserSelected(user.id)"
                          @click.stop="toggleUserSelection(user.id)"
                        />
                        <label class="flex-1 cursor-pointer text-sm">
                          {{ user.name }}
                        </label>
                      </div>
                      <div v-if="users.length === 0" class="p-4 text-center text-sm text-gray-500">
                        No users found
                      </div>
                    </div>
                  </PopoverContent>
                </Popover>

                <!-- Selected Users Pills for Team -->
                <div v-if="filterType === 'team' && selectedUsers.length > 0" class="flex flex-wrap gap-2 mt-2">
                  <Badge v-for="userId in selectedUsers" :key="userId" variant="secondary" class="pl-2 pr-1">
                    {{ users.find(u => u.id === userId)?.name }}
                    <Button
                      variant="ghost"
                      size="sm"
                      class="h-4 w-4 p-0 ml-1 hover:bg-transparent"
                      @click="removeUser(userId)"
                    >
                      <X class="h-3 w-3" />
                    </Button>
                  </Badge>
                </div>

                <!-- Single select for Project and User -->
                <Select v-if="filterType !== 'team'" v-model="selectedFilter">
                  <SelectTrigger class="h-11">
                    <SelectValue :placeholder="`Choose a ${filterType}`" />
                  </SelectTrigger>
                  <SelectContent>
                    <template v-if="filterType === 'project'">
                      <SelectItem v-for="project in projects" :key="project.id" :value="project.id">
                        {{ project.name }}
                      </SelectItem>
                    </template>
                    <template v-else>
                      <SelectItem v-for="user in users" :key="user.id" :value="user.id">
                        {{ user.name }}
                      </SelectItem>
                    </template>
                  </SelectContent>
                </Select>
              </div>

              <!-- Time Period (only for team reports) -->
              <div v-if="filterType === 'team'" class="space-y-2">
                <label class="text-sm font-medium text-gray-700 flex items-center gap-2">
                  <Calendar class="w-4 h-4" />
                  Time Period
                </label>
                <Select v-model="timePeriod">
                  <SelectTrigger class="h-11">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="week">
                      <div class="flex items-center gap-2">
                        <Calendar class="w-4 h-4" />
                        This Week
                      </div>
                    </SelectItem>
                    <SelectItem value="month">
                      <div class="flex items-center gap-2">
                        <Calendar class="w-4 h-4" />
                        This Month
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <!-- Permission Notice for Team Reports -->
            <Alert v-if="filterType === 'team' && !canGenerateTeamReports" variant="destructive">
              <AlertCircle class="h-4 w-4" />
              <AlertDescription>
                You don't have permission to generate team reports. Only Managers, HR, and Admins can access this feature.
              </AlertDescription>
            </Alert>

            <Separator />

            <Button @click="handleGenerateReport" 
              :disabled="(filterType === 'team' ? selectedUsers.length === 0 : !selectedFilter) || generating || (filterType === 'team' && !canGenerateTeamReports)"
              class="w-full md:w-auto h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium">
              <template v-if="generating">
                <div class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                Generating...
              </template>
              <template v-else>
                <FileText class="w-4 h-4 mr-2" />
                Generate Report
              </template>
            </Button>
          </CardContent>
        </Card>

        <!-- Report Display -->
        <div v-if="currentReport" class="space-y-6 animate-in fade-in duration-500">
          <!-- Report Header -->
          <Card class="border-0 shadow-lg bg-gradient-to-r from-blue-600 to-blue-700 text-white">
            <CardContent class="p-6">
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <FileText class="w-6 h-6" />
                    <h2 class="text-2xl font-bold">Report #{{ currentReport.id }}</h2>
                  </div>
                  <p class="text-blue-100">
                    {{ currentReport.filterType === 'user' ? 'User Report' : currentReport.filterType === 'team' ? 'Team Summary Report' : 'Project Report' }} • {{
                    currentReport.filterName
                    }}
                  </p>
                  <p class="text-sm text-blue-200 mt-1 flex items-center gap-1">
                    <Calendar class="w-4 h-4" />
                    Generated on {{ formatDate(currentReport.timestamp) }}
                  </p>
                  <p v-if="currentReport.filterType === 'team'" class="text-sm text-blue-200 mt-1">
                    Period: {{ formatDeadline(currentReport.periodStart!) }} - {{ formatDeadline(currentReport.periodEnd!) }}
                  </p>
                </div>

                <div class="flex gap-3">
                  <Button @click="exportToPDF" variant="secondary"
                    class="h-11 bg-white text-blue-600 hover:bg-blue-50 font-medium">
                    <Download class="w-4 h-4 mr-2" />
                    Export PDF
                  </Button>
                  <Button @click="exportToExcel" variant="secondary"
                    class="h-11 bg-white text-blue-600 hover:bg-blue-50 font-medium">
                    <Download class="w-4 h-4 mr-2" />
                    Export Excel
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- Statistics -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <Card v-for="stat in statsCards" :key="stat.label"
              class="border-0 shadow-sm bg-gradient-to-br from-white to-gray-50">
              <CardContent class="p-6">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-600">{{ stat.label }}</span>
                  <div
                    :class="`w-8 h-8 rounded-full ${stat.color} flex items-center justify-center text-white text-sm font-bold`">
                    {{ stat.icon }}
                  </div>
                </div>
                <div class="text-3xl font-bold text-gray-900">{{ stat.value }}</div>
                <div class="text-xs text-gray-500 mt-1">
                  {{ getPercentage(stat.value) }} of total
                </div>
              </CardContent>
            </Card>
          </div>

          <!-- Task Table -->
          <Card v-if="currentReport.tasks.length > 0" class="border-0 shadow-sm">
            <CardHeader>
              <CardTitle class="text-lg">Task Details</CardTitle>
              <CardDescription>Showing {{ currentReport.tasks.length }} tasks for {{ currentReport.filterName }}
                <span v-if="currentReport.filterType === 'team'">
                  ({{ currentReport.timePeriod === 'week' ? 'This Week' : 'This Month' }})
                </span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div class="overflow-x-auto">
                <table class="w-full">
                  <thead>
                    <tr class="border-b border-gray-200">
                      <th v-if="currentReport.filterType === 'user' || currentReport.filterType === 'team'"
                        class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Project</th>
                      <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Task Name</th>
                      <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                      <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Priority</th>
                      <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Deadline</th>
                      <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">Assigned To</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="task in currentReport.tasks" :key="task.id"
                      class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                      <td v-if="currentReport.filterType === 'user' || currentReport.filterType === 'team'" class="py-3 px-4">
                        <div class="font-medium text-gray-900">{{ task.project.name }}</div>
                      </td>
                      <td class="py-3 px-4">
                        <div class="font-medium text-gray-900">{{ task.name }}</div>
                        <div v-if="task.desc" class="text-sm text-gray-500 mt-1">{{ task.desc }}</div>
                      </td>
                      <td class="py-3 px-4">
                        <div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold"
                          :class="getStatusBadge(task.status)">
                          {{ task.status }}
                        </div>
                      </td>
                      <td class="py-3 px-4">
                        <span :class="`font-semibold ${getPriorityColor(task.priorityLevel)}`">
                          {{ task.priorityLevel }}
                        </span>
                      </td>
                      <td class="py-3 px-4 text-sm text-gray-600">
                        {{ formatDeadline(task.deadline) }}
                      </td>
                      <td class="py-3 px-4">
                        <div class="flex flex-wrap gap-1">
                          <Badge v-for="collab in task.collaborators" :key="collab.id" variant="outline"
                            class="text-xs">
                            {{ collab.name }}
                          </Badge>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <!-- No Tasks Alert -->
          <Alert v-else>
            <AlertCircle class="h-4 w-4" />
            <AlertDescription>No tasks found for the selected filter{{ currentReport.filterType === 'team' ? ' and time period' : '' }}.</AlertDescription>
          </Alert>
        </div>

        <!-- No Report State -->
        <Card v-else class="border-0 shadow-lg bg-white">
          <CardContent class="p-12 text-center">
            <div class="flex flex-col items-center gap-4">
              <div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center">
                <FileText class="w-10 h-10 text-gray-400" />
              </div>
              <div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">No Report Generated</h3>
                <p class="text-gray-600 max-w-md">
                  Select your filter criteria above and click "Generate Report" to create a comprehensive task
                  completion
                  report.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </template>
    </div>
  </div>
</template>