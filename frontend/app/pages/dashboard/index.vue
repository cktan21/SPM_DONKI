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
  isOwned?: boolean // true = user owns this project, false = user is collaborator
}

// User data
const userData = useState<{ user: User }>("userData")
const user = computed(() => userData.value.user)

// Projects
const projects = ref<Project[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// Fetch projects created by the user
const fetchOwnedProjects = async (userId: string): Promise<Project[]> => {
  const res = await fetch(`http://127.0.0.1:4100/uid/${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })

  if (!res.ok) throw new Error(`Failed to fetch owned projects: ${res.status}`)
  const data = await res.json()
  
  // Mark these as owned projects
  return (data.projects || []).map((p: Project) => ({ 
    ...p, 
    isOwned: true 
  }))
}

// Fetch tasks where user is a collaborator and extract their projects
const fetchCollaboratorProjects = async (userId: string): Promise<Project[]> => {
  const res = await fetch(`http://127.0.0.1:4000/tasks/user/${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })

  if (!res.ok) throw new Error(`Failed to fetch collaborator tasks: ${res.status}`)
  const data = await res.json()
  console.log(data)

  // Extract unique projects from tasks where user is a collaborator
  const projectMap = new Map<string, Project>()

  for (const taskEntry of data.tasks || []) {
    const task = taskEntry.task
    const collaborators = task?.collaborators || []

    // Skip tasks where user is not a collaborator
    if (!collaborators.includes(userId)) continue

    // Extract actual project object
    const projectData = taskEntry.project?.project
    if (!projectData || !projectData.id) continue

    // Add to map if not already present
    if (!projectMap.has(projectData.id)) {
      projectMap.set(projectData.id, {
        id: projectData.id,
        uid: projectData.uid || "",
        name: projectData.name || "Unnamed Project",
        desc: projectData.desc || null,
        created_at: projectData.created_at || new Date().toISOString(),
        tasks: [],
        isOwned: false
      })
    }
  }

  return Array.from(projectMap.values())
}

// Main fetch function
const fetchProjects = async () => {
  if (!user.value?.id) return

  loading.value = true
  error.value = null

  try {
    // Fetch owned projects and collaborator projects in parallel
    const [ownedProjects, collaboratorProjects] = await Promise.all([
      fetchOwnedProjects(user.value.id),
      fetchCollaboratorProjects(user.value.id),
    ])

    // Filter out collaborator projects that the user already owns
    const ownedProjectIds = new Set(ownedProjects.map(p => p.id))
    const uniqueCollaboratorProjects = collaboratorProjects.filter(
      p => !ownedProjectIds.has(p.id)
    )

    // Combine owned projects first, then collaborator projects
    projects.value = [...ownedProjects, ...uniqueCollaboratorProjects]

    console.log(`Loaded ${ownedProjects.length} owned projects and ${uniqueCollaboratorProjects.length} collaborator projects`)
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