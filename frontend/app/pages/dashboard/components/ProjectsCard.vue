<script setup lang="ts">
import { useRouter } from "vue-router"

// 🧩 Define Task & Project interfaces
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
  priorityLabel: string
}

interface Project {
  id: string
  uid: string
  name: string
  desc?: string | null
  created_at: string
  tasks?: Task[]
}

// 🧩 Props
const props = defineProps<{
  projects: Project[]
  loading: boolean
  error: string | null
}>()

// 🧩 Router instance
const router = useRouter()

/**
 * Navigate to /task page and pass full project object
 * Use casting to satisfy TypeScript
 */
function openProject(project: Project) {
  router.push({
    path: "/task",
    state: { project } as unknown as Record<string, any>,
  })
}
</script>

<template>
  <div class="w-full">
    <!-- Loading State -->
    <div v-if="props.loading" class="text-center py-10 text-gray-500">
      Loading projects...
    </div>

    <!-- Error State -->
    <div
      v-else-if="props.error"
      class="text-center py-10 text-red-500 font-medium"
    >
      {{ props.error }}
    </div>

    <!-- Empty State -->
    <div
      v-else-if="!props.projects || props.projects.length === 0"
      class="text-center py-10 text-gray-500"
    >
      No projects found.
    </div>

    <!-- Projects Grid -->
    <div
      v-else
      class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4"
    >
      <div
        v-for="project in props.projects"
        :key="project.id"
        class="p-5 bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer"
        @click="openProject(project)"
      >
        <!-- Project Header -->
        <div class="flex flex-col gap-1">
          <h3 class="font-semibold text-lg text-gray-800">
            {{ project.name }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ project.desc || "No description available" }}
          </p>
        </div>

        <!-- Divider -->
        <hr class="my-3 border-gray-200" />

        <!-- Project Details -->
        <div class="text-sm text-gray-600 space-y-1">
          <p>
            <span class="font-medium text-gray-700">ID:</span>
            {{ project.id }}
          </p>
          <p>
            <span class="font-medium text-gray-700">User ID:</span>
            {{ project.uid }}
          </p>
          <p>
            <span class="font-medium text-gray-700">Created At:</span>
            {{ new Date(project.created_at).toLocaleString() }}
          </p>
          <p>
            <span class="font-medium text-gray-700">Tasks:</span>
            {{ project.tasks?.length ?? 0 }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hover effect */
div[class*="bg-white"]:hover {
  transform: translateY(-2px);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
</style>
