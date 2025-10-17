<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import type { DateValue } from "@internationalized/date"
import { getLocalTimeZone } from "@internationalized/date"

// Shadcn UI components
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

import { useToast } from "@/components/ui/toast"

import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover"

import { Calendar } from "@/components/ui/calendar"

const router = useRouter()
const { toast } = useToast()
const API_BASE_URL = "http://localhost:4000"

const formCreate = ref({
  name: "",
  pid: "",
  parentTaskId: "",
  collaboratorsCsv: "",
  desc: "",
  notes: "",
  schedule: {
    status: "",
    priority: "",
    deadline: undefined as DateValue | undefined,
  },
})

const state = ref({ creating: false })
const handleBack = () => router.back()

const createTask = async () => {
  if (!formCreate.value.name.trim()) {
    toast({ title: "Task name is required", variant: "destructive" })
    return
  }

  try {
    state.value.creating = true

    const collaborators = formCreate.value.collaboratorsCsv
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)

    const schedule: any = {}
    if (formCreate.value.schedule.status)
      schedule.status = formCreate.value.schedule.status
    if (formCreate.value.schedule.priority)
      schedule.priority = formCreate.value.schedule.priority
    if (formCreate.value.schedule.deadline)
      schedule.deadline = formCreate.value.schedule.deadline
        .toDate(getLocalTimeZone())
        .toISOString()

    const payload: any = {
      name: formCreate.value.name,
      desc: formCreate.value.desc || undefined,
      notes: formCreate.value.notes || undefined,
      pid: formCreate.value.pid || undefined,
      parentTaskId: formCreate.value.parentTaskId || undefined,
      collaborators: collaborators.length > 0 ? collaborators : undefined,
      schedule: Object.keys(schedule).length > 0 ? schedule : undefined,
    }

    const response = await fetch(`${API_BASE_URL}/createTask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })

    if (!response.ok) throw new Error(`Failed: ${response.statusText}`)

    toast({ title: "Task created successfully!" })
    router.push("/task")
  } catch (err: any) {
    toast({ title: "Error creating task", description: err.message, variant: "destructive" })
  } finally {
    state.value.creating = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-background">
    <div class="container max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 lg:py-12">
      <!-- Back Button -->
      <Button
        variant="ghost"
        @click="handleBack"
        class="mb-6 -ml-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back
      </Button>

      <!-- Form Card -->
      <Card>
        <CardHeader>
          <CardTitle class="text-2xl sm:text-3xl">Create New Task</CardTitle>
          <CardDescription>
            Fill in the details below to create a new task for your project
          </CardDescription>
        </CardHeader>
        <CardContent class="pt-6">
          <form @submit.prevent="createTask" class="space-y-6">
            <!-- Task Information Section -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Task Information</h3>
              
              <div class="grid gap-4 sm:gap-6">
                <div class="space-y-2">
                  <Label for="task-name" class="text-sm font-medium">
                    Task Name <span class="text-destructive">*</span>
                  </Label>
                  <Input 
                    id="task-name" 
                    v-model="formCreate.name" 
                    placeholder="Enter a descriptive task name" 
                    required 
                    class="w-full"
                  />
                </div>

                <div class="grid gap-4 sm:grid-cols-2">
                  <div class="space-y-2">
                    <Label for="task-pid" class="text-sm font-medium">Project ID</Label>
                    <Input 
                      id="task-pid" 
                      v-model="formCreate.pid" 
                      placeholder="Optional project identifier" 
                      class="w-full"
                    />
                  </div>
                  <div class="space-y-2">
                    <Label for="task-parent" class="text-sm font-medium">Parent Task ID</Label>
                    <Input 
                      id="task-parent" 
                      v-model="formCreate.parentTaskId" 
                      placeholder="Optional parent task" 
                      class="w-full"
                    />
                  </div>
                </div>

                <div class="space-y-2">
                  <Label for="task-description" class="text-sm font-medium">Description</Label>
                  <Textarea
                    id="task-description"
                    v-model="formCreate.desc"
                    placeholder="Describe the task purpose, requirements, and any important details..."
                    class="resize-none min-h-[100px] w-full"
                    rows="4"
                  />
                </div>

                <div class="space-y-2">
                  <Label for="task-notes" class="text-sm font-medium">Additional Notes</Label>
                  <Input 
                    id="task-notes" 
                    v-model="formCreate.notes" 
                    placeholder="Any extra information or reminders" 
                    class="w-full"
                  />
                </div>

                <div class="space-y-2">
                  <Label for="task-collaborators" class="text-sm font-medium">Collaborators</Label>
                  <Input 
                    id="task-collaborators" 
                    v-model="formCreate.collaboratorsCsv" 
                    placeholder="Comma-separated UUIDs (e.g., uuid1, uuid2, uuid3)" 
                    class="w-full"
                  />
                  <p class="text-xs text-muted-foreground">
                    Enter user IDs separated by commas
                  </p>
                </div>
              </div>
            </div>

            <Separator />

            <!-- Schedule Section -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Schedule & Priority</h3>
              
              <div class="grid gap-4 sm:grid-cols-3">
                <div class="space-y-2">
                  <Label for="task-status" class="text-sm font-medium">Status</Label>
                  <Select v-model="formCreate.schedule.status">
                    <SelectTrigger id="task-status" class="w-full">
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="todo">To-do</SelectItem>
                      <SelectItem value="in_progress">In Progress</SelectItem>
                      <SelectItem value="done">Done</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <Label for="task-priority" class="text-sm font-medium">Priority (1-10)</Label>
                    <Popover>
                      <PopoverTrigger as-child>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          class="h-5 w-5 rounded-full p-0"
                          type="button"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent class="w-auto p-3 text-sm" :align="'start'">
                        <p class="font-semibold mb-1">Priority Scale</p>
                        <p class="text-muted-foreground">1 = Lowest priority</p>
                        <p class="text-muted-foreground">10 = Highest priority</p>
                      </PopoverContent>
                    </Popover>
                  </div>
                  <Input 
                    id="task-priority" 
                    v-model.number="formCreate.schedule.priority" 
                    type="number"
                    min="1"
                    max="10"
                    placeholder="1-10" 
                    class="w-full"
                  />
                </div>

                <div class="space-y-2">
                  <Label for="task-deadline" class="text-sm font-medium">Deadline</Label>
                  <Popover>
                    <PopoverTrigger as-child>
                      <Button 
                        variant="outline" 
                        class="w-full justify-start text-left font-normal"
                        id="task-deadline"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span class="flex-1 truncate">
                          {{
                            formCreate.schedule.deadline
                              ? formCreate.schedule.deadline
                                  .toDate(getLocalTimeZone())
                                  .toLocaleDateString()
                              : "Pick a date"
                          }}
                        </span>
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent class="w-auto p-0" :align="'start'">
                      <Calendar
                        :model-value="formCreate.schedule.deadline as DateValue | undefined"
                        @update:model-value="(value: DateValue | undefined) => formCreate.schedule.deadline = value"
                        :initial-focus="true"
                      />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>
            </div>

            <Separator />

            <!-- Action Buttons -->
            <div class="flex flex-col-reverse sm:flex-row sm:justify-end gap-3 pt-2">
              <Button 
                variant="outline" 
                type="button" 
                @click="handleBack"
                class="w-full sm:w-auto"
              >
                Cancel
              </Button>
              <Button 
                type="submit" 
                :disabled="state.creating"
                class="w-full sm:w-auto"
              >
                <svg v-if="state.creating" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span v-if="state.creating">Creating Task...</span>
                <span v-else>Create Task</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>