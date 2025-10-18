<script lang="ts">
export const description = "A sidebar that collapses to icons."
export const iframeHeight = "800px"
export const containerClass = "w-full h-full"
</script>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue"
import AppSidebar from "./components/AppSidebar.vue"
import DashboardCards from "./components/ProjectsCard.vue"

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

// Interfaces
interface User {
  id: string
  name?: string
  email?: string
  role?: string
}

interface Project {
  id: string
  uid: string
  name: string
  desc?: string | null
  created_at: string
  tasks: any[]
}

// User data
const userData = useState<{ user: User }>("userData")
const user = computed(() => userData.value.user)

// Projects
const projects = ref<Project[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// Fetch projects
const fetchProjects = async () => {
  if (!user.value?.id) return

  loading.value = true
  error.value = null

  try {
    const res = await fetch(`http://127.0.0.1:4100/uid/${user.value.id}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })

    if (!res.ok) throw new Error(`Failed to fetch projects: ${res.status}`)
    const data = await res.json()
    projects.value = data.projects || []
  } catch (err: any) {
    console.error("Error fetching projects:", err)
    error.value = err.message || "Failed to fetch projects"
  } finally {
    loading.value = false
  }
}

// Fetch on mount
onMounted(() => {
  fetchProjects()
})
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <header class="flex h-16 shrink-0 items-center gap-2 px-4">
        <SidebarTrigger class="-ml-1" />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block" />
            <BreadcrumbItem>
              <BreadcrumbPage>Projects</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </header>

      <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
        <!-- DashboardCards now handles navigation internally -->
        <DashboardCards
          :projects="projects"
          :loading="loading"
          :error="error"
        />
        <div class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
