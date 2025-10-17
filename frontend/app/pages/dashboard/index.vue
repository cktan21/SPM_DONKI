<script lang="ts">
export const description = "A sidebar that collapses to icons."
export const iframeHeight = "800px"
export const containerClass = "w-full h-full"
</script>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue"
import { useRouter } from "vue-router"

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

// 🧩 Interfaces
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

// 🧩 Router & Global user state
const router = useRouter()
const userData = useState<{ user: User }>("userData")
const user = computed(() => userData.value.user)

// 🧩 Reactive data
const projects = ref<Project[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// 🧩 Global project state to pass between pages
const selectedProject = useState<Project | null>("selectedProject")

// 🧩 Fetch user projects
const fetchProjects = async () => {
  if (!user.value?.id) {
    console.warn("⚠️ No user ID found — skipping project fetch.")
    return
  }

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
    console.error("❌ Error fetching projects:", err)
    error.value = err.message || "Failed to fetch projects"
  } finally {
    loading.value = false
  }
}

// 🧩 Handle navigation — store project globally before redirect
const goToTaskPage = (project: Project) => {
  selectedProject.value = project
  router.push("/task")
}

// 🧩 Fetch on mount
onMounted(() => {
  console.log("Fetching projects for user:", user.value)
  fetchProjects()
})
</script>

<template>
  <SidebarProvider>
    <AppSidebar />

    <SidebarInset>
      <!-- 🧭 Header -->
      <header
        class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear
        group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
      >
        <div class="flex items-center gap-2 px-4">
          <SidebarTrigger class="-ml-1" />
          <Separator orientation="vertical" class="mr-2 h-4" />
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
        </div>
      </header>

      <!-- 🧩 Main Content -->
      <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
        <DashboardCards
          :projects="projects"
          :loading="loading"
          :error="error"
          @project-clicked="goToTaskPage"
        />

        <div class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
