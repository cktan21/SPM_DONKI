<script setup lang="ts">
import { computed } from "vue"
import { useRouter } from "vue-router"
import { useState } from "#imports"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertTriangle, CheckCircle2, Clock, TrendingUp } from "lucide-vue-next"

interface Schedule {
  tid: string
  sid: string
  deadline: string | null
  status: string | null
  created_at: string
  is_recurring: boolean
  next_occurrence: string | null
  start: string | null
  frequency: string | null
}

interface Task {
  id: string
  name: string
  created_by_uid: string
  updated_timestamp: string
  parentTaskId: string | null
  collaborators: string[] | null
  pid: string
  desc: string
  notes: string
  priorityLevel: number
  label: string
  status?: string | null
  deadline?: string | null
  is_recurring?: boolean | null
  next_occurrence?: string | null
  start?: string | null
  sid?: string | null
  schedule?: Schedule | { message: string }
}

interface Project {
  id: string
  uid: string
  name: string
  desc?: string | null
  created_at: string
  user_name?: string | null
  tasks?: Task[]
}

const props = defineProps<{
  projects: Project[]
  loading: boolean
  error: string | null
}>()

const router = useRouter()
const selectedProject = useState<Project | null>("selectedProject")

// Helper: Get most common label from project tasks
function getProjectLabel(project: Project): string | null {
  const tasks = project.tasks || []
  if (tasks.length === 0) return null
  
  const labelCounts: Record<string, number> = {}
  tasks.forEach(task => {
    if (task.label) {
      labelCounts[task.label] = (labelCounts[task.label] || 0) + 1
    }
  })
  
  const mostCommonLabel = Object.entries(labelCounts)
    .sort((a, b) => b[1] - a[1])[0]
  
  return mostCommonLabel ? mostCommonLabel[0] : null
}

// Helper: Format project ID
function formatProjectId(id: string): string {
  if (id.length <= 14) return id
  return `${id.slice(0, 7)}...${id.slice(-7)}`
}

// Helper: Get task status from schedule object
function getTaskStatus(task: Task): string | null {
  if (task.schedule && 'status' in task.schedule) {
    return task.schedule.status
  }
  return task.status || null
}

// Helper: Get task deadline
function getTaskDeadline(task: Task): string | null {
  if (task.schedule && 'deadline' in task.schedule) {
    return task.schedule.deadline
  }
  return task.deadline || null
}

// Helper: Check if task is overdue
function isTaskOverdue(task: Task): boolean {
  const deadline = getTaskDeadline(task)
  const status = getTaskStatus(task)
  
  if (!deadline || status === "done") return false
  
  return new Date(deadline) < new Date()
}

// Helper: Get priority color
function getPriorityColor(level: number): string {
  if (level >= 8) return "bg-red-500"
  if (level >= 6) return "bg-orange-500"
  if (level >= 4) return "bg-yellow-500"
  return "bg-green-500"
}

// Helper: Get status badge variant
function getStatusBadgeClass(status: string | null): string {
  if (!status) return "bg-gray-100 text-gray-600 border-gray-200"
  
  switch (status.toLowerCase()) {
    case "done":
      return "bg-emerald-50 text-emerald-700 border-emerald-200"
    case "ongoing":
      return "bg-blue-50 text-blue-700 border-blue-200"
    case "todo":
    case "to do":
      return "bg-orange-50 text-orange-700 border-orange-200"
    default:
      return "bg-gray-100 text-gray-600 border-gray-200"
  }
}

// Calculate project metrics
function calculateMetrics(project: Project) {
  const tasks = project.tasks || []
  const totalTasks = tasks.length
  
  if (totalTasks === 0) {
    return {
      totalTasks: 0,
      completedTasks: 0,
      todoTasks: 0,
      ongoingTasks: 0,
      completionPercentage: 0,
      overdueTasks: 0,
      avgPriority: 0,
      hasRisks: false
    }
  }
  
  const completedTasks = tasks.filter(t => getTaskStatus(t) === "done").length
  const todoTasks = tasks.filter(t => {
    const status = getTaskStatus(t)
    return status === "todo" || status === "to do"
  }).length
  const ongoingTasks = tasks.filter(t => getTaskStatus(t) === "ongoing").length
  const overdueTasks = tasks.filter(t => isTaskOverdue(t)).length
  
  const avgPriority = tasks.reduce((sum, t) => sum + (t.priorityLevel || 0), 0) / totalTasks
  const completionPercentage = Math.round((completedTasks / totalTasks) * 100)
  
  return {
    totalTasks,
    completedTasks,
    todoTasks,
    ongoingTasks,
    completionPercentage,
    overdueTasks,
    avgPriority,
    hasRisks: overdueTasks > 0
  }
}

function openProject(project: Project) {
  selectedProject.value = project
  router.push(`/project/${project.id}`)
}
</script>

<template>
  <div class="w-full">
    <!-- Loading State -->
    <div v-if="props.loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-3">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-gray-900"></div>
        <p class="text-sm text-gray-500">Loading projects...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="props.error" class="py-10">
      <Alert variant="destructive">
        <AlertTriangle class="h-4 w-4" />
        <AlertDescription>{{ props.error }}</AlertDescription>
      </Alert>
    </div>

    <!-- Empty State -->
    <div v-else-if="!props.projects || props.projects.length === 0" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-3 text-center">
        <div class="text-6xl">🎉</div>
        <h3 class="text-2xl font-semibold text-gray-900">All Clear!</h3>
        <p class="text-gray-600 text-base">You don't have any ongoing projects right now</p>
        <p class="text-gray-500 text-sm">Time to relax or start something new</p>
      </div>
    </div>

    <!-- Projects Grid -->
    <div v-else class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
      <Card
        v-for="project in props.projects"
        :key="project.id"
        class="group cursor-pointer transition-all duration-200 hover:shadow-lg hover:-translate-y-1 border-gray-200"
        @click="openProject(project)"
      >
        <CardHeader class="pb-3">
          <div class="flex items-start justify-between gap-2">
            <div class="flex-1 min-w-0">
              <CardTitle class="text-lg font-semibold text-gray-900 truncate">
                {{ project.name }}
              </CardTitle>
              <CardDescription class="text-sm text-gray-500 line-clamp-2 mt-1">
                {{ project.desc || "No description available" }}
              </CardDescription>
            </div>
            
            <!-- Risk Indicator -->
            <AlertTriangle 
              v-if="calculateMetrics(project).hasRisks"
              class="h-5 w-5 text-red-500 flex-shrink-0"
            />
          </div>
        </CardHeader>

        <CardContent class="space-y-4">
          <!-- Progress Section -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600 font-medium">Progress</span>
              <span class="text-gray-900 font-semibold">
                {{ calculateMetrics(project).completionPercentage }}%
              </span>
            </div>
            <Progress 
              :model-value="calculateMetrics(project).completionPercentage" 
              class="h-2"
            />
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-3 gap-3">
            <!-- Total Tasks -->
            <div class="flex flex-col items-center justify-center p-3 bg-gray-50 rounded-lg">
              <div class="text-2xl font-bold text-gray-900">
                {{ calculateMetrics(project).totalTasks }}
              </div>
              <div class="text-xs text-gray-500 mt-0.5">Total</div>
            </div>

            <!-- Completed Tasks -->
            <div class="flex flex-col items-center justify-center p-3 bg-emerald-50 rounded-lg">
              <div class="text-2xl font-bold text-emerald-700">
                {{ calculateMetrics(project).completedTasks }}
              </div>
              <div class="text-xs text-emerald-600 mt-0.5">Done</div>
            </div>

            <!-- Overdue Tasks -->
            <div class="flex flex-col items-center justify-center p-3 bg-red-50 rounded-lg">
              <div class="text-2xl font-bold text-red-700">
                {{ calculateMetrics(project).overdueTasks }}
              </div>
              <div class="text-xs text-red-600 mt-0.5">Overdue</div>
            </div>
          </div>

          <!-- Status Breakdown -->
          <div class="flex items-center gap-2 flex-wrap">
            <Badge 
              variant="outline" 
              class="bg-orange-50 text-orange-700 border-orange-200 text-xs"
            >
              To Do: {{ calculateMetrics(project).todoTasks }}
            </Badge>
            <Badge 
              variant="outline" 
              class="bg-blue-50 text-blue-700 border-blue-200 text-xs"
            >
              Ongoing: {{ calculateMetrics(project).ongoingTasks }}
            </Badge>
            <Badge 
              v-if="getProjectLabel(project)"
              variant="outline" 
              class="text-xs"
            >
              {{ getProjectLabel(project) }}
            </Badge>
          </div>

          <!-- Priority Indicator -->
          <div class="space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-600 font-medium">Avg Priority</span>
              <span class="text-gray-900 font-semibold">
                {{ calculateMetrics(project).avgPriority.toFixed(1) }}/10
              </span>
            </div>
            <div class="flex gap-1">
              <div 
                v-for="i in 10" 
                :key="i"
                class="h-1.5 flex-1 rounded-full transition-all"
                :class="i <= Math.round(calculateMetrics(project).avgPriority) 
                  ? getPriorityColor(Math.round(calculateMetrics(project).avgPriority))
                  : 'bg-gray-200'"
              ></div>
            </div>
          </div>

          <!-- Footer Info -->
          <div class="pt-3 border-t border-gray-100 space-y-1.5">
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-500">Created By:</span>
              <span class="text-gray-700 font-bold">{{ project.user_name || "Null" }}</span>
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-500">Project ID:</span>
              <span class="text-gray-700 font-bold">{{ formatProjectId(project.id) }}</span>
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-500">Created On:</span>
              <span class="text-gray-700 font-bold">{{ new Date(project.created_at).toLocaleDateString() }}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>