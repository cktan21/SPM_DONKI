<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft, TriangleAlert } from "lucide-vue-next";

// Import custom components
import TaskHeader from "./components/TaskHeader.vue";
import TaskDetails from "./components/TaskDetails.vue";
import TaskContent from "./components/TaskContent.vue";
import SubtasksList from "./components/SubtasksList.vue";
import TaskChat from "./components/TaskChat.vue";
import TaskChangelog from "./components/TaskChangelog.vue";

const route = useRoute();
const router = useRouter();
const taskId = computed(() => route.params.id as string);

// Cache task data by ID for instant loading
const getCachedTask = (id: string) => {
    const cacheKey = `task_${id}`;
    return useState<any>(cacheKey, () => null);
};

const getCachedChangelog = (id: string) => {
    const cacheKey = `task_changelog_${id}`;
    return useState<any[]>(cacheKey, () => []);
};

const task = ref<any>(null);
const changelog = ref<any[]>([]);
const loading = ref(false);
const refreshing = ref(false); // Separate flag for background refresh
const error = ref<string | null>(null);
const deleteDialogOpen = ref(false);
const itemToDelete = ref<{ id: string; type: "task" | "subtask" } | null>(null);

const API_BASE_URL = "http://localhost:8000/manage-task";
const TASK_BASE_URL = "http://localhost:8000/tasks";

// User permissions
const userData = useState<any>("userData");
const role = userData.value?.user?.role;
const uid = userData.value?.user?.id;

const canEditTask = computed(() => {
    if (!task.value) return false;
    return role === "manager" || uid === task.value.created_by_uid;
});

// Helpers
const isUuid = (v: string) => typeof v === "string" && v.trim().length === 36;

const normalizeTask = (x: any) => {
    if (!x) return null;
    return {
        ...x,
        status: x?.status || x?.schedule?.status || "not started",
        deadline: x?.deadline || x?.schedule?.deadline || null
    };
};

const normalizeSubtask = (x: any) => {
    return {
        id: x?.id ?? "",
        name: x?.name ?? "Untitled",
        desc: x?.desc ?? "",
        notes: x?.notes ?? "",
        priorityLevel: x?.priorityLevel ?? undefined,
        label: x?.label ?? "",
        status: x?.status ?? "not started",
        deadline: x?.deadline ?? "",
        parentTaskId: x?.parentTaskId ?? null,
        pid: x?.pid ?? null,
        collaborators: Array.isArray(x?.collaborators) ? x.collaborators : [],
        created_by_uid: x?.created_by_uid ?? null,
        updated_timestamp: x?.updated_timestamp ?? null
    };
};

// API Fetchers
const fetchMainTask = async (id: string) => {
    const res = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`Task fetch failed (${res.status})`);
    const text = await res.text();
    if (!text) throw new Error("Empty response");

    const data = JSON.parse(text);
    const rawTask = data?.task ?? (data?.id ? data : null);
    return normalizeTask(rawTask);
};

const fetchSubtasks = async (id: string) => {
    const res = await fetch(`${TASK_BASE_URL}/ptid/${id}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`Subtasks fetch failed (${res.status})`);
    const text = await res.text();
    if (!text) return [];

    const data = JSON.parse(text);
    const list = Array.isArray(data?.tasks)
        ? data.tasks
        : Array.isArray(data)
        ? data
        : [];
    return list.map(normalizeSubtask);
};

const fetchChangelog = async (id: string) => {
    try {
        const res = await fetch(`${TASK_BASE_URL}/logs/${id}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!res.ok) return [];
        const text = await res.text();
        if (!text) return [];

        const data = JSON.parse(text);
        return Array.isArray(data?.log) ? data.log : [];
    } catch (e) {
        console.error("Failed to fetch changelog:", e);
        return [];
    }
};

const fetchTask = async (backgroundRefresh = false) => {
    const id = String(taskId.value || "").trim();
    if (!isUuid(id)) {
        error.value = "Invalid task ID (must be a 36-char UUID)";
        return;
    }

    // Set appropriate loading flags
    if (backgroundRefresh) {
        refreshing.value = true;
    } else {
        loading.value = true;
    }
    error.value = null;

    try {
        const [main, subs, logs] = await Promise.all([
            fetchMainTask(id),
            fetchSubtasks(id),
            fetchChangelog(id)
        ]);

        if (!main) {
            error.value = "Task not found";
            task.value = null;
            return;
        }

        const updatedTask = {
            ...main,
            subtasks: subs
        };

        // Update both local state and cache
        task.value = updatedTask;
        changelog.value = logs;

        // Cache the task data
        const cachedTask = getCachedTask(id);
        const cachedLogs = getCachedChangelog(id);
        cachedTask.value = updatedTask;
        cachedLogs.value = logs;
    } catch (e: any) {
        console.error(e);
        error.value = e?.message || "Failed to load task";
        // Don't clear cache on error - keep showing stale data
    } finally {
        loading.value = false;
        refreshing.value = false;
    }
};

const openDeleteDialog = (id: string, type: "task" | "subtask") => {
    itemToDelete.value = { id, type };
    deleteDialogOpen.value = true;
};

const confirmDelete = async () => {
    if (!itemToDelete.value) return;

    try {
        // Backend DELETE endpoint is /{task_id} (not /tasks/{task_id})
        const response = await fetch(
            `${API_BASE_URL}/${itemToDelete.value.id}`,
            {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            }
        );

        if (!response.ok) {
            const errorText = await response.text().catch(() => "");
            let errorMessage = `Failed to delete (${response.status})`;
            try {
                const errorData = JSON.parse(errorText);
                errorMessage =
                    errorData.detail || errorData.message || errorMessage;
            } catch {
                if (errorText) errorMessage = errorText;
            }
            throw new Error(errorMessage);
        }

        if (itemToDelete.value.type === "task") {
            // Redirect to project page if available, otherwise dashboard
            const projectId = task.value?.pid;
            if (projectId) {
                router.push(`/project/${projectId}`);
            } else {
                router.push("/dashboard");
            }
        } else {
            // Refresh task data after deleting subtask
            await fetchTask();
        }
    } catch (err: any) {
        console.error("Delete error:", err);
        alert("Error deleting: " + err.message);
    } finally {
        deleteDialogOpen.value = false;
        itemToDelete.value = null;
    }
};

const goToEditPage = (id: string) => {
    router.push(`/task/edit/${id}`);
};

onMounted(async () => {
    const id = String(taskId.value || "").trim();

    if (!isUuid(id)) {
        error.value = "Invalid task ID (must be a 36-char UUID)";
        return;
    }

    // Check for cached data
    const cachedTask = getCachedTask(id);
    const cachedLogs = getCachedChangelog(id);

    if (cachedTask.value) {
        // Show cached data immediately
        task.value = cachedTask.value;
        changelog.value = cachedLogs.value;
        console.log("Loaded cached task:", id);
        // Fetch fresh data in background
        await fetchTask(true); // true = background refresh
    } else {
        // No cache, do normal fetch
        await fetchTask(false);
    }
});
</script>

<template>
    <div class="min-h-screen bg-slate-50/50 dark:bg-slate-950">
        <div class="container mx-auto max-w-7xl py-8 px-4 sm:px-6 lg:px-8">
            <!-- Back Button & Refresh Indicator -->
            <div class="mb-6 flex items-center justify-between">
                <Button
                    variant="ghost"
                    size="sm"
                    @click="router.back()"
                    class="gap-2 -ml-2 hover:bg-slate-100 dark:hover:bg-slate-900">
                    <ArrowLeft class="w-4 h-4" />
                    <span>Back</span>
                </Button>
                <!-- Refresh indicator -->
                <div
                    v-if="refreshing"
                    class="flex items-center gap-2 text-sm text-muted-foreground">
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
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="space-y-6">
                <Card class="border-0 shadow-sm">
                    <CardHeader>
                        <Skeleton class="h-10 w-3/4 mb-2" />
                        <Skeleton class="h-4 w-1/2" />
                    </CardHeader>
                    <CardContent>
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            <div class="lg:col-span-2">
                                <Skeleton class="h-32 w-full" />
                            </div>
                            <div>
                                <Skeleton class="h-64 w-full" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <!-- Error State -->
            <Alert
                v-else-if="error"
                variant="destructive"
                class="border-0 shadow-sm">
                <TriangleAlert class="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{{ error }}</AlertDescription>
            </Alert>

            <!-- Main Content -->
            <div v-else-if="task" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Left Column: Main Content -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Task Header -->
                    <TaskHeader
                        :task="task"
                        :can-edit="canEditTask"
                        @edit="goToEditPage(task.id)"
                        @delete="openDeleteDialog(task.id, 'task')" />

                    <!-- Task Content (Description & Notes) -->
                    <TaskContent :task="task" />

                    <!-- Task Details Card (Mobile Only) -->
                    <div class="lg:hidden">
                        <TaskDetails :task="task" />
                    </div>

                    <!-- Subtasks -->
                    <SubtasksList
                        :subtasks="task.subtasks"
                        :user-id="uid"
                        :user-role="role"
                        @edit="goToEditPage"
                        @delete="(id: string) => openDeleteDialog(id, 'subtask')" />

                    <!-- Chat -->
                    <TaskChat :task-id="taskId" />

                    <!-- Changelog -->
                    <TaskChangelog :changelog="changelog" />
                </div>

                <!-- Right Column: Details Sidebar (Desktop Only) -->
                <div class="hidden lg:block">
                    <TaskDetails :task="task" class="sticky top-6" />
                </div>
            </div>

            <!-- No Data State -->
            <div v-else class="flex items-center justify-center py-20">
                <Card class="w-full max-w-md border-0 shadow-sm">
                    <CardContent class="pt-6 text-center">
                        <TriangleAlert
                            class="w-12 h-12 text-slate-400 mx-auto mb-3 dark:text-slate-600" />
                        <p
                            class="text-lg font-semibold text-slate-900 dark:text-slate-100">
                            No task data found
                        </p>
                        <p
                            class="text-sm text-slate-600 mt-1 dark:text-slate-400">
                            The task you're looking for doesn't exist
                        </p>
                    </CardContent>
                </Card>
            </div>
        </div>

        <!-- Delete Confirmation Dialog -->
        <AlertDialog v-model:open="deleteDialogOpen">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                    <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete the
                        {{
                            itemToDelete?.type === "task"
                                ? "task and all its subtasks"
                                : "subtask"
                        }}.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction
                        @click="confirmDelete"
                        class="bg-red-600 hover:bg-red-700 focus:ring-red-600">
                        Delete
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    </div>
</template>
