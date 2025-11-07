<script lang="ts">
export const description = "A sidebar that collapses to icons.";
export const iframeHeight = "800px";
export const containerClass = "w-full h-full";
</script>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import AppSidebar from "./components/AppSidebar.vue";
import DashboardCards from "./components/ProjectsCard.vue";

import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator
} from "@/components/ui/breadcrumb";

import { Separator } from "@/components/ui/separator";
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger
} from "@/components/ui/sidebar";

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { X, SlidersHorizontal, Plus } from "lucide-vue-next";

// Interfaces
interface User {
    id: string;
    name?: string;
    email?: string;
    role?: string;
}

interface Project {
    id: string;
    uid: string;
    name: string;
    desc?: string | null;
    created_at: string;
    updated_at?: string | null;
    user_name?: string | null;
    owner_name?: string | null;
    department?: string | null;
    tasks: any[];
    isOwned?: boolean;
}

type HealthStatus = "on-track" | "at-risk" | "delayed";

// User data
const userData = useState<{ user: User }>("userData");
const user = computed(() => userData.value.user);

// Projects - Use cached state for instant loading
const cachedProjects = useState<Project[]>("dashboardProjects", () => []);
const projects = ref<Project[]>([]);
const loading = ref(false);
const refreshing = ref(false); // Separate flag for background refresh
const error = ref<string | null>(null);

// Filters & Sorting
const selectedStatus = ref<string>("all");
const selectedLabel = ref<string>("all");
const selectedDepartment = ref<string>("all");
const selectedHealth = ref<string>("all");
const sortBy = ref<string>("health");

// Cache for user names to avoid redundant API calls
const userNameCache = new Map<string, string>();

// Fetch user name from internal API
const fetchUserName = async (userId: string): Promise<string> => {
    // Check cache first
    if (userNameCache.has(userId)) {
        return userNameCache.get(userId)!;
    }

    try {
        const res = await fetch(`http://127.0.0.1:5100/internal/${userId}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!res.ok) {
            console.warn(
                `Failed to fetch user name for ${userId}: ${res.status}`
            );
            return "Unknown User";
        }

        const data = await res.json();
        const userName = data.name || "Unknown User";

        // Cache the result
        userNameCache.set(userId, userName);
        return userName;
    } catch (err) {
        console.warn(`Error fetching user name for ${userId}:`, err);
        return "Unknown User";
    }
};

// Fetch projects created by the user
const fetchOwnedProjects = async (userId: string): Promise<Project[]> => {
    try {
        const res = await fetch(`http://127.0.0.1:4100/uid/${userId}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        if (!res.ok) {
            console.warn(`No owned projects found for user: ${res.status}`);
            return [];
        }
        const data = await res.json();
        return (data.projects || []).map((p: Project) => ({
            ...p,
            isOwned: true,
            user_name: data.user_name || ""
        }));
    } catch (err) {
        console.warn("Failed to fetch owned projects:", err);
        return [];
    }
};

// Main fetch function - OPTIMIZED with parallel fetching
const fetchProjects = async (backgroundRefresh = false) => {
    if (!user.value?.id) return;

    // Set appropriate loading flags
    if (backgroundRefresh) {
        refreshing.value = true;
    } else {
        loading.value = true;
    }
    error.value = null;

    try {
        // Fetch projects
        const ownedProjects = await fetchOwnedProjects(user.value.id);

        // Extract unique user IDs that need names
        const userIds = new Set<string>();
        ownedProjects.forEach((project) => {
            if (project.uid && !userNameCache.has(project.uid)) {
                userIds.add(project.uid);
            }
        });

        // Fetch all user names in parallel
        if (userIds.size > 0) {
            await Promise.all(
                Array.from(userIds).map((uid) => fetchUserName(uid))
            );
        }

        // Assign owner names from cache
        const updatedProjects = ownedProjects.map((project) => ({
            ...project,
            owner_name: userNameCache.get(project.uid) || project.user_name
        }));

        // Update both local state and cache
        projects.value = updatedProjects;
        cachedProjects.value = updatedProjects;

        if (updatedProjects.length === 0) {
            error.value = null;
        }
    } catch (err: any) {
        console.error("Error fetching projects:", err);
        error.value = err.message || "Failed to fetch projects";
        // Don't clear cache on error - keep showing stale data
    } finally {
        loading.value = false;
        refreshing.value = false;
    }
};

// Helper: Get task status from schedule
function getTaskStatus(task: any): string | null {
    if (task.schedule && "status" in task.schedule) {
        return task.schedule.status;
    }
    return task.status || null;
}

// Helper: Get task deadline
function getTaskDeadline(task: any): string | null {
    if (task.schedule && "deadline" in task.schedule) {
        return task.schedule.deadline;
    }
    return task.deadline || null;
}

// Helper: Get task start
function getTaskStart(task: any): string | null {
    if (task.schedule && "start" in task.schedule) {
        return task.schedule.start;
    }
    return task.start || null;
}

// Helper: Get most common label from project
function getProjectLabel(project: Project): string | null {
    const tasks = project.tasks || [];
    if (tasks.length === 0) return null;

    const labelCounts: Record<string, number> = {};
    for (const task of tasks) {
        if (task.label) {
            labelCounts[task.label] = (labelCounts[task.label] || 0) + 1;
        }
    }

    const entries = Object.entries(labelCounts);
    if (entries.length === 0) return null;

    const [mostCommonLabel] = entries.sort((a, b) => b[1] - a[1])[0]!;
    return mostCommonLabel;
}

// Helper: Check if project has status
function projectHasStatus(project: Project, status: string): boolean {
    const tasks = project.tasks || [];
    return tasks.some((task) => {
        const taskStatus = getTaskStatus(task);
        return taskStatus?.toLowerCase() === status.toLowerCase();
    });
}

// Helper: Get earliest deadline
function getEarliestDeadline(project: Project): Date | null {
    const tasks = project.tasks || [];
    const deadlines = tasks
        .map((task) => getTaskDeadline(task))
        .filter((d) => d !== null)
        .map((d) => new Date(d!));

    if (deadlines.length === 0) return null;
    return new Date(Math.min(...deadlines.map((d) => d.getTime())));
}

// Helper: Calculate completion percentage
function getCompletionPercentage(project: Project): number {
    const tasks = project.tasks || [];
    if (tasks.length === 0) return 0;

    const completedTasks = tasks.filter(
        (t) => getTaskStatus(t) === "done"
    ).length;
    return Math.round((completedTasks / tasks.length) * 100);
}

// Helper: Get project health status
function getProjectHealth(project: Project): HealthStatus {
    const tasks = project.tasks || [];

    if (tasks.length === 0) return "on-track";

    const now = new Date();
    const completionPercentage = getCompletionPercentage(project);
    const earliestDeadline = getEarliestDeadline(project);

    // Delayed: deadline passed and not 100% complete
    if (
        earliestDeadline &&
        earliestDeadline < now &&
        completionPercentage < 100
    ) {
        return "delayed";
    }

    // At Risk: < 50% complete and > 75% of time elapsed
    if (earliestDeadline) {
        const startDates = tasks
            .map((task) => getTaskStart(task))
            .filter((d) => d !== null)
            .map((d) => new Date(d!));

        if (startDates.length > 0) {
            const earliestStart = new Date(
                Math.min(...startDates.map((d) => d.getTime()))
            );
            const totalTime =
                earliestDeadline.getTime() - earliestStart.getTime();
            const elapsedTime = now.getTime() - earliestStart.getTime();
            const timeProgress =
                totalTime > 0 ? (elapsedTime / totalTime) * 100 : 0;

            if (completionPercentage < 50 && timeProgress > 75) {
                return "at-risk";
            }
        }
    }

    return "on-track";
}

// Computed: Available filter options
const availableLabels = computed(() => {
    const labels = new Set<string>();
    projects.value.forEach((project) => {
        const label = getProjectLabel(project);
        if (label) labels.add(label);
    });
    return Array.from(labels);
});

const availableDepartments = computed(() => {
    const departments = new Set<string>();
    projects.value.forEach((project) => {
        if (project.department) departments.add(project.department);
    });
    return Array.from(departments);
});

// Computed: Filtered and sorted projects
const filteredAndSortedProjects = computed(() => {
    let filtered = [...projects.value];

    // Apply status filter
    if (selectedStatus.value !== "all") {
        filtered = filtered.filter((project) =>
            projectHasStatus(project, selectedStatus.value)
        );
    }

    // Apply label filter
    if (selectedLabel.value !== "all") {
        filtered = filtered.filter(
            (project) => getProjectLabel(project) === selectedLabel.value
        );
    }

    // Apply department filter
    if (selectedDepartment.value !== "all") {
        filtered = filtered.filter(
            (project) => project.department === selectedDepartment.value
        );
    }

    // Apply health filter
    if (selectedHealth.value !== "all") {
        filtered = filtered.filter(
            (project) => getProjectHealth(project) === selectedHealth.value
        );
    }

    // Apply sorting
    filtered.sort((a, b) => {
        switch (sortBy.value) {
            case "deadline":
                const deadlineA = getEarliestDeadline(a);
                const deadlineB = getEarliestDeadline(b);
                if (!deadlineA) return 1;
                if (!deadlineB) return -1;
                return deadlineA.getTime() - deadlineB.getTime();

            case "oldest":
                return (
                    new Date(a.created_at).getTime() -
                    new Date(b.created_at).getTime()
                );

            case "most-todo":
                const todoA = (a.tasks || []).filter((t) => {
                    const status = getTaskStatus(t);
                    return status === "todo" || status === "to do";
                }).length;
                const todoB = (b.tasks || []).filter((t) => {
                    const status = getTaskStatus(t);
                    return status === "todo" || status === "to do";
                }).length;
                return todoB - todoA;

            case "least-done":
                const doneA = (a.tasks || []).filter(
                    (t) => getTaskStatus(t) === "done"
                ).length;
                const doneB = (b.tasks || []).filter(
                    (t) => getTaskStatus(t) === "done"
                ).length;
                return doneA - doneB;

            case "priority":
                const avgPriorityA =
                    (a.tasks || []).reduce(
                        (sum, t) => sum + (t.priorityLevel || 0),
                        0
                    ) / (a.tasks?.length || 1);
                const avgPriorityB =
                    (b.tasks || []).reduce(
                        (sum, t) => sum + (t.priorityLevel || 0),
                        0
                    ) / (b.tasks?.length || 1);
                return avgPriorityB - avgPriorityA;

            case "health":
                const healthOrder = { delayed: 0, "at-risk": 1, "on-track": 2 };
                return (
                    healthOrder[getProjectHealth(a)] -
                    healthOrder[getProjectHealth(b)]
                );

            default:
                return 0;
        }
    });

    return filtered;
});

// Computed: Active filters count
const activeFiltersCount = computed(() => {
    let count = 0;
    if (selectedStatus.value !== "all") count++;
    if (selectedLabel.value !== "all") count++;
    if (selectedDepartment.value !== "all") count++;
    if (selectedHealth.value !== "all") count++;
    return count;
});

// Clear all filters
function clearFilters() {
    selectedStatus.value = "all";
    selectedLabel.value = "all";
    selectedDepartment.value = "all";
    selectedHealth.value = "all";
}

// Fetch on mount - Load cached data immediately, then refresh in background
onMounted(() => {
    // Show cached projects immediately if available
    if (cachedProjects.value.length > 0) {
        projects.value = cachedProjects.value;
        console.log("Loaded cached projects:", cachedProjects.value.length);
        // Fetch fresh data in background
        fetchProjects(true); // true = background refresh
    } else {
        // No cache, do normal fetch
        fetchProjects(false);
    }
});
</script>

<template>
    <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
            <header class="flex h-16 shrink-0 items-center gap-2 px-4 border-b">
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
                <!-- Refresh indicator -->
                <div
                    v-if="refreshing"
                    class="ml-auto flex items-center gap-2 text-sm text-muted-foreground">
                    <svg
                        class="h-4 w-4 animate-spin"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24">
                        <circle
                            class="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            stroke-width="4"></circle>
                        <path
                            class="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span class="hidden sm:inline">Refreshing...</span>
                </div>
            </header>

            <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
                <!-- Filters & Sorting Section -->
                <div class="flex flex-col gap-3 pt-4">
                    <!-- Filter Row -->
                    <div
                        class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
                        <div class="flex items-center gap-2">
                            <SlidersHorizontal class="h-4 w-4 text-gray-500" />
                            <span class="text-sm font-medium text-gray-700"
                                >Filters</span
                            >
                            <Badge
                                v-if="activeFiltersCount > 0"
                                variant="secondary"
                                class="text-xs">
                                {{ activeFiltersCount }}
                            </Badge>
                        </div>

                        <div class="flex flex-wrap gap-2 w-full sm:w-auto">
                            <!-- Health Status Filter -->
                            <Select v-model="selectedHealth">
                                <SelectTrigger class="w-[140px] h-9 text-sm">
                                    <SelectValue placeholder="Health" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all"
                                        >All Health</SelectItem
                                    >
                                    <SelectItem value="on-track"
                                        >On Track</SelectItem
                                    >
                                    <SelectItem value="at-risk"
                                        >At Risk</SelectItem
                                    >
                                    <SelectItem value="delayed"
                                        >Delayed</SelectItem
                                    >
                                </SelectContent>
                            </Select>

                            <!-- Status Filter -->
                            <Select v-model="selectedStatus">
                                <SelectTrigger class="w-[140px] h-9 text-sm">
                                    <SelectValue placeholder="Status" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all"
                                        >All Status</SelectItem
                                    >
                                    <SelectItem value="todo">To Do</SelectItem>
                                    <SelectItem value="ongoing"
                                        >Ongoing</SelectItem
                                    >
                                    <SelectItem value="done">Done</SelectItem>
                                </SelectContent>
                            </Select>

                            <!-- Label Filter -->
                            <Select
                                v-model="selectedLabel"
                                :disabled="availableLabels.length === 0">
                                <SelectTrigger class="w-[140px] h-9 text-sm">
                                    <SelectValue placeholder="Label" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all"
                                        >All Labels</SelectItem
                                    >
                                    <SelectItem
                                        v-for="label in availableLabels"
                                        :key="label"
                                        :value="label">
                                        {{ label }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>

                            <!-- Department Filter -->
                            <Select
                                v-model="selectedDepartment"
                                :disabled="availableDepartments.length === 0">
                                <SelectTrigger class="w-[140px] h-9 text-sm">
                                    <SelectValue placeholder="Department" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all"
                                        >All Departments</SelectItem
                                    >
                                    <SelectItem
                                        v-for="dept in availableDepartments"
                                        :key="dept"
                                        :value="dept">
                                        {{ dept }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>

                            <!-- Clear Filters -->
                            <Button
                                v-if="activeFiltersCount > 0"
                                variant="ghost"
                                size="sm"
                                class="h-9 text-sm"
                                @click="clearFilters">
                                <X class="h-4 w-4 mr-1" />
                                Clear
                            </Button>
                        </div>
                    </div>

                    <!-- Sort Row -->
                    <div class="flex items-center justify-between gap-2">
                        <div class="flex items-center gap-2">
                            <span class="text-sm text-gray-600">Sort by:</span>
                            <Select v-model="sortBy">
                                <SelectTrigger class="w-[180px] h-9 text-sm">
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="health"
                                        >Health Status</SelectItem
                                    >
                                    <SelectItem value="deadline"
                                        >Nearest Deadline</SelectItem
                                    >
                                    <SelectItem value="oldest"
                                        >Oldest First</SelectItem
                                    >
                                    <SelectItem value="most-todo"
                                        >Most To Do</SelectItem
                                    >
                                    <SelectItem value="least-done"
                                        >Least Done</SelectItem
                                    >
                                    <SelectItem value="priority"
                                        >Highest Priority</SelectItem
                                    >
                                </SelectContent>
                            </Select>
                        </div>
                        <!-- Create Project Button -->
                        <Button
                            @click="navigateTo('/project/createProject')"
                            class="gap-2">
                            <Plus class="h-4 w-4" />
                            Create Project
                        </Button>
                    </div>
                </div>

                <!-- Results Count -->
                <div
                    v-if="!loading && filteredAndSortedProjects.length > 0"
                    class="text-sm text-gray-600">
                    Showing {{ filteredAndSortedProjects.length }}
                    {{
                        filteredAndSortedProjects.length === 1
                            ? "project"
                            : "projects"
                    }}
                </div>

                <!-- Dashboard Cards -->
                <DashboardCards
                    :projects="filteredAndSortedProjects"
                    :loading="loading"
                    :error="error" />

                <div
                    class="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
            </div>
        </SidebarInset>
    </SidebarProvider>
</template>
