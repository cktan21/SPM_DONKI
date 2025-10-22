<script setup lang="ts">
import { ref, shallowRef, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { parseDate, type DateValue, getLocalTimeZone } from "@internationalized/date"

// Shadcn UI components
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useToast } from "@/components/ui/toast"
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover"
import { Calendar } from "@/components/ui/calendar"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { TriangleAlert, Loader2, ArrowLeft } from "lucide-vue-next"

// --- Setup ---
const router = useRouter()
const route = useRoute()
const { toast } = useToast()
const taskId = ref(route.params.id as string)
const API_BASE_URL = "http://localhost:4000"

// --- Form State ---
const formEdit = ref({
  name: "",
  pid: "",
  parentTaskId: "",
  collaboratorsCsv: "",
  desc: "",
  notes: "",
  status: "",
  priorityLabel: "",
})

// Separate ref for deadline to avoid reactivity type issues
const deadline = shallowRef<DateValue | undefined>(undefined)

// --- Page State ---
const state = ref({
  loading: false,
  saving: false,
  error: null as string | null,
})

const handleBack = () => router.back()

// --- Fetch Task Data ---
const fetchTaskData = async () => {
  state.value.loading = true
  state.value.error = null
  try {
    const res = await fetch(`${API_BASE_URL}/tasks/${taskId.value}`)
    if (!res.ok) throw new Error(`Failed to fetch task details: ${res.statusText}`)
    const data = await res.json()
    const task = data?.task ?? data
    if (!task) throw new Error("Task data not found in response.")

    // Fill form fields
    formEdit.value.name = task.name || ""
    formEdit.value.pid = task.pid || ""
    formEdit.value.parentTaskId = task.parentTaskId || ""
    formEdit.value.desc = task.desc || ""
    formEdit.value.notes = task.notes || ""
    formEdit.value.status = task.schedule?.status || task.status || ""
    formEdit.value.priorityLabel = task.priorityLabel || ""

    // Convert ISO string to DateValue
    const deadlineISO = task.schedule?.deadline || task.deadline
    deadline.value = deadlineISO ? parseDate(deadlineISO.slice(0, 10)) : undefined

    // Convert collaborators array to CSV string
    if (Array.isArray(task.collaborators)) {
      formEdit.value.collaboratorsCsv = task.collaborators
        .map((c: any) => (typeof c === "string" ? c : c?.id))
        .filter(Boolean)
        .join(", ")
    }
  } catch (err: any) {
    state.value.error = err.message
  } finally {
    state.value.loading = false
  }
}

// --- Update Task ---
const updateTask = async () => {
  if (!formEdit.value.name.trim()) {
    toast({ title: "Task name is required", variant: "destructive" })
    return
  }

  try {
    state.value.saving = true

    const collaborators = formEdit.value.collaboratorsCsv
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)

    const payload: any = {
      name: formEdit.value.name,
      desc: formEdit.value.desc || undefined,
      notes: formEdit.value.notes || undefined,
      priorityLabel: formEdit.value.priorityLabel || undefined,
      status: formEdit.value.status || undefined,
      deadline: deadline.value
        ? deadline.value.toDate(getLocalTimeZone()).toISOString()
        : undefined,
      collaborators: collaborators.length > 0 ? collaborators : undefined,
    }

    const response = await fetch(`${API_BASE_URL}/tasks/${taskId.value}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
    if (!response.ok) throw new Error(`Failed: ${response.statusText}`)

    toast({ title: "Task updated successfully!" })
    router.push(`/task/${taskId.value}`)
  } catch (err: any) {
    toast({ title: "Error updating task", description: err.message, variant: "destructive" })
  } finally {
    state.value.saving = false
  }
}

onMounted(fetchTaskData)
</script>

<template>
  <div class="min-h-screen bg-background">
    <div class="container max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 lg:py-12">
      <Button variant="ghost" @click="handleBack" class="mb-6 -ml-2" :disabled="state.saving">
        <ArrowLeft class="h-4 w-4 mr-2" /> Back
      </Button>

      <Card>
        <CardHeader>
          <CardTitle class="text-2xl sm:text-3xl">Edit Task</CardTitle>
          <CardDescription>Update the details for your task</CardDescription>
        </CardHeader>

        <CardContent class="pt-6">
          <div v-if="state.loading" class="flex justify-center items-center h-48">
            <Loader2 class="h-8 w-8 animate-spin text-muted-foreground" />
          </div>

          <Alert v-else-if="state.error" variant="destructive">
            <TriangleAlert class="h-4 w-4" />
            <AlertTitle>Error Loading Task</AlertTitle>
            <AlertDescription>{{ state.error }}</AlertDescription>
          </Alert>

          <form v-else @submit.prevent="updateTask" class="space-y-6">
            <!-- Task Info -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Task Information</h3>
              <div class="grid gap-4 sm:gap-6">
                <div class="space-y-2">
                  <Label for="task-name" class="text-sm font-medium">Task Name <span class="text-destructive">*</span></Label>
                  <Input id="task-name" v-model="formEdit.name" placeholder="Enter a descriptive task name" required class="w-full"/>
                </div>

                <div class="grid gap-4 sm:grid-cols-2">
                  <div class="space-y-2">
                    <Label for="task-pid" class="text-sm font-medium">Project ID</Label>
                    <Input id="task-pid" v-model="formEdit.pid" class="w-full" disabled/>
                  </div>
                  <div class="space-y-2">
                    <Label for="task-parent" class="text-sm font-medium">Parent Task ID</Label>
                    <Input id="task-parent" v-model="formEdit.parentTaskId" class="w-full" disabled/>
                  </div>
                </div>

                <div class="space-y-2">
                  <Label for="task-description" class="text-sm font-medium">Description</Label>
                  <Textarea id="task-description" v-model="formEdit.desc" placeholder="Describe the task purpose, requirements, and any important details..." class="resize-none min-h-[100px] w-full" rows="4"/>
                </div>

                <div class="space-y-2">
                  <Label for="task-notes" class="text-sm font-medium">Additional Notes</Label>
                  <Input id="task-notes" v-model="formEdit.notes" placeholder="Any extra information or reminders" class="w-full"/>
                </div>

                <div class="space-y-2">
                  <Label for="task-collaborators" class="text-sm font-medium">Collaborators</Label>
                  <Input id="task-collaborators" v-model="formEdit.collaboratorsCsv" placeholder="Comma-separated UUIDs" class="w-full"/>
                  <p class="text-xs text-muted-foreground">Enter user IDs separated by commas</p>
                </div>
              </div>
            </div>

            <Separator />

            <!-- Schedule & Priority -->
            <div class="space-y-4">
              <h3 class="text-lg font-semibold">Schedule & Priority</h3>
              <div class="grid gap-4 sm:grid-cols-3">
                <div class="space-y-2">
                  <Label for="task-status" class="text-sm font-medium">Status</Label>
                  <Select v-model="formEdit.status">
                    <SelectTrigger id="task-status" class="w-full"><SelectValue placeholder="Select status"/></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="not started">Not Started</SelectItem>
                      <SelectItem value="ongoing">Ongoing</SelectItem>
                      <SelectItem value="completed">Completed</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div class="space-y-2">
                  <Label for="task-priority" class="text-sm font-medium">Priority Label</Label>
                  <Input id="task-priority" v-model="formEdit.priorityLabel" placeholder="e.g. High, Medium, Low" class="w-full"/>
                </div>

                <div class="space-y-2">
                  <Label for="task-deadline" class="text-sm font-medium">Deadline</Label>
                  <Popover>
                    <PopoverTrigger as-child>
                      <Button variant="outline" class="w-full justify-start text-left font-normal">
                        <span class="flex-1 truncate">{{ deadline ? deadline.toDate(getLocalTimeZone()).toLocaleDateString() : "Pick a date" }}</span>
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent class="w-auto p-0" :align="'start'">
                      <Calendar
                        v-model="deadline"
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
              <Button variant="outline" type="button" @click="handleBack" class="w-full sm:w-auto" :disabled="state.saving">Cancel</Button>
              <Button type="submit" :disabled="state.saving" class="w-full sm:w-auto">
                <Loader2 v-if="state.saving" class="h-4 w-4 mr-2 animate-spin"/>
                <span v-if="state.saving">Saving Changes...</span>
                <span v-else>Save Changes</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>