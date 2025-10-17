<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"

const router = useRouter()

const API_BASE_URL = 'http://localhost:4000'

const formCreate = ref({
  name: '',
  pid: '',
  parentTaskId: '',
  collaboratorsCsv: '',
  desc: '',
  notes: '',
  schedule: {
    status: '',
    priority: '',
    deadline: ''
  }
})

const state = ref({
  creating: false
})

const handleBack = () => {
  router.back()
}

const createTask = async () => {
  if (!formCreate.value.name.trim()) {
    alert('Task name is required')
    return
  }

  try {
    state.value.creating = true

    // Parse collaborators
    const collaborators = formCreate.value.collaboratorsCsv
      .split(',')
      .map(s => s.trim())
      .filter(Boolean)

    // Build schedule object, only include if values are set
    const schedule: any = {}
    if (formCreate.value.schedule.status) schedule.status = formCreate.value.schedule.status
    if (formCreate.value.schedule.priority) schedule.priority = formCreate.value.schedule.priority
    if (formCreate.value.schedule.deadline) schedule.deadline = formCreate.value.schedule.deadline

    const payload: any = {
      name: formCreate.value.name,
    }

    // Only add optional fields if they have values
    if (formCreate.value.desc) payload.desc = formCreate.value.desc
    if (formCreate.value.notes) payload.notes = formCreate.value.notes
    if (formCreate.value.pid) payload.pid = formCreate.value.pid
    if (formCreate.value.parentTaskId) payload.parentTaskId = formCreate.value.parentTaskId
    if (collaborators.length > 0) payload.collaborators = collaborators
    if (Object.keys(schedule).length > 0) payload.schedule = schedule

    console.log('Creating task with payload:', JSON.stringify(payload, null, 2))

    const response = await fetch(`${API_BASE_URL}/createTask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Error response:', errorText)
      throw new Error(`Failed to create task: ${response.status} - ${errorText}`)
    }

    const result = await response.json()
    console.log('Task created:', result)

    // Navigate back to task list
    router.push('/task')
  } catch (err: any) {
    console.error(err)
    alert('Error creating task: ' + err.message)
  } finally {
    state.value.creating = false
  }
}
</script>

<template>
  <div class="min-h-screen p-4 sm:p-6 lg:p-8">
    <div class="max-w-2xl mx-auto">
      <!-- Back Button -->
      <button 
        @click="router.back()"
        class="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 mb-6"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
             viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="mr-2">
          <path d="m15 18-6-6 6-6" />
        </svg>
        Back to tasks
      </button>

      <form @submit.prevent="createTask">
        <FieldGroup>
          <FieldSet>
            <FieldLegend>Create Task</FieldLegend>
            <FieldDescription>
              Fill in the details to create a new task
            </FieldDescription>
            
            <FieldGroup>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Field>
                  <FieldLabel for="task-name">Name</FieldLabel>
                  <Input
                    id="task-name"
                    v-model="formCreate.name"
                    placeholder="Task name"
                    required
                  />
                </Field>
                
                <Field>
                  <FieldLabel for="task-pid">PID (Project ID)</FieldLabel>
                  <Input
                    id="task-pid"
                    v-model="formCreate.pid"
                    placeholder="optional"
                  />
                </Field>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Field>
                  <FieldLabel for="task-parent">Parent Task ID</FieldLabel>
                  <Input
                    id="task-parent"
                    v-model="formCreate.parentTaskId"
                    placeholder="optional"
                  />
                </Field>
                
                <Field>
                  <FieldLabel for="task-collaborators">Collaborators (CSV of UUIDs)</FieldLabel>
                  <Input
                    id="task-collaborators"
                    v-model="formCreate.collaboratorsCsv"
                    placeholder="id1,id2,..."
                  />
                </Field>
              </div>

              <Field>
                <FieldLabel for="task-description">Description</FieldLabel>
                <Textarea
                  id="task-description"
                  v-model="formCreate.desc"
                  placeholder="Task description"
                  rows="3"
                  class="resize-none"
                />
              </Field>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Field>
                  <FieldLabel for="task-notes">Notes</FieldLabel>
                  <Input
                    id="task-notes"
                    v-model="formCreate.notes"
                    placeholder="Additional notes"
                  />
                </Field>
                
                <Field>
                  <FieldLabel for="task-status">Schedule Status</FieldLabel>
                  <Select v-model="formCreate.schedule.status">
                    <SelectTrigger id="task-status">
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="todo">todo</SelectItem>
                      <SelectItem value="in_progress">in_progress</SelectItem>
                      <SelectItem value="done">done</SelectItem>
                    </SelectContent>
                  </Select>
                </Field>
                
                <Field>
                  <FieldLabel for="task-priority">Priority</FieldLabel>
                  <Select v-model="formCreate.schedule.priority">
                    <SelectTrigger id="task-priority">
                      <SelectValue placeholder="Select priority" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">low</SelectItem>
                      <SelectItem value="medium">medium</SelectItem>
                      <SelectItem value="high">high</SelectItem>
                    </SelectContent>
                  </Select>
                </Field>
              </div>

              <Field>
                <FieldLabel for="task-deadline">Deadline (ISO)</FieldLabel>
                <Input
                  id="task-deadline"
                  v-model="formCreate.schedule.deadline"
                  type="datetime-local"
                />
                <FieldDescription>
                  Select the deadline for this task
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldSet>

          <Field orientation="horizontal" class="justify-end">
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
              {{ state.creating ? 'Creating…' : 'Create' }}
            </Button>
          </Field>
        </FieldGroup>
      </form>
    </div>
  </div>
</template>2d