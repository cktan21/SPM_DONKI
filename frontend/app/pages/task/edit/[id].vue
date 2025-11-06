<script setup lang="ts">
import { ref, shallowRef, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
    parseDate,
    type DateValue,
    getLocalTimeZone,
    CalendarDate
} from "@internationalized/date";

// Shadcn UI components
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";
import { useToast } from "@/components/ui/toast";
import {
    Popover,
    PopoverTrigger,
    PopoverContent
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import {
    TriangleAlert,
    Loader2,
    ArrowLeft,
    Clock,
    Plus,
    X,
    Timer
} from "lucide-vue-next";

// --- Setup ---
const router = useRouter();
const route = useRoute();
const { toast } = useToast();
const taskId = ref(route.params.id as string);
const API_BASE_URL = "http://localhost:4000";
const COMPOSITE_API_URL = "http://localhost:4100";

// Get authenticated user data from middleware
const userData = useState<any>("userData");

// --- Authorization State ---
const canEditAll = ref(false);
const canEditCollaborators = ref(false);

// --- Time Logger State ---
interface TimeEntry {
    id: string;
    hours: number;
    minutes: number;
    description: string;
    date: string;
    userId: string;
    userName: string;
}

const timeEntries = ref<TimeEntry[]>([]);
const newTimeEntry = ref({
    hours: 0,
    minutes: 0,
    description: ""
});
const isAddingTime = ref(false);

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
    priorityLevel: "",
    label: "",
    createdByUid: "",
    isRecurring: "false",
    frequency: ""
});

// Separate refs for dates
const startDate = shallowRef<DateValue | undefined>(undefined);
const deadline = shallowRef<DateValue | undefined>(undefined);

// Time refs (default to UTC+8 times)
const startTime = ref("09:00"); // Default to 9:00 AM UTC+8
const deadlineTime = ref("17:00"); // Default to 5:00 PM UTC+8

// --- Page State ---
const state = ref({
    loading: false,
    saving: false,
    error: null as string | null
});

// --- Collaborators State ---
const selectedCollaborators = ref<string[]>([]);
const allUsers = ref<{ id: string; name: string }[]>([]);
const isCollaboratorPopoverOpen = ref(false);
const searchQuery = ref("");

// --- Parent Task State ---
const projectTasks = ref<{ id: string; name: string }[]>([]);
const isParentTaskPopoverOpen = ref(false);
const parentTaskSearchQuery = ref("");

// --- Time Logger Computed ---
const totalTimeSpent = computed(() => {
    const total = timeEntries.value.reduce((acc, entry) => {
        return acc + entry.hours * 60 + entry.minutes;
    }, 0);

    const hours = Math.floor(total / 60);
    const minutes = total % 60;

    return { hours, minutes, total };
});

const formattedTotalTime = computed(() => {
    const { hours, minutes } = totalTimeSpent.value;
    if (hours === 0 && minutes === 0) return "No time logged";
    if (hours === 0) return `${minutes}m`;
    if (minutes === 0) return `${hours}h`;
    return `${hours}h ${minutes}m`;
});

const handleBack = () => router.back();

const getUserName = (id: string) =>
    allUsers.value.find((u) => u.id === id)?.name || id;

const getTaskName = (id: string) =>
    projectTasks.value.find((t) => t.id === id)?.name || id;

const filteredUsers = computed(() =>
    allUsers.value.filter((u) =>
        u.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
);

const filteredTasks = computed(() =>
    projectTasks.value.filter(
        (t) =>
            t.name
                .toLowerCase()
                .includes(parentTaskSearchQuery.value.toLowerCase()) &&
            t.id !== taskId.value
    )
);

const selectUser = (id: string) => {
    if (!selectedCollaborators.value.includes(id)) {
        selectedCollaborators.value.push(id);
        formEdit.value.collaboratorsCsv =
            selectedCollaborators.value.join(", ");
    }
    isCollaboratorPopoverOpen.value = false;
    searchQuery.value = "";
};

const removeCollaborator = (id: string) => {
    selectedCollaborators.value = selectedCollaborators.value.filter(
        (x) => x !== id
    );
    formEdit.value.collaboratorsCsv = selectedCollaborators.value.join(", ");
};

const selectParentTask = (id: string) => {
    formEdit.value.parentTaskId = id;
    isParentTaskPopoverOpen.value = false;
    parentTaskSearchQuery.value = "";
};

const clearParentTask = () => {
    formEdit.value.parentTaskId = "";
};

// Helper function to format date
const formatDate = (dateValue: any): string => {
    if (!dateValue) return "Pick a date";

    try {
        const date = dateValue.toDate(getLocalTimeZone());
        const day = String(date.getDate()).padStart(2, "0");
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const year = date.getFullYear();

        return `${day}/${month}/${year}`;
    } catch (e) {
        return "Pick a date";
    }
};

// Validate date range (including time)
const isDateRangeValid = computed(() => {
    if (!startDate.value || !deadline.value) {
        return true;
    }

    const start = startDate.value.toDate(getLocalTimeZone());
    const end = deadline.value.toDate(getLocalTimeZone());

    // If dates are the same, check times
    if (start.toDateString() === end.toDateString()) {
        return startTime.value < deadlineTime.value;
    }

    return start < end;
});

// Check if deadline is in the past
const isDeadlinePast = computed(() => {
    if (!deadline.value) return false;

    const deadlineDate = deadline.value.toDate(getLocalTimeZone());
    const now = new Date();

    // Set both to start of day for comparison
    deadlineDate.setHours(0, 0, 0, 0);
    now.setHours(0, 0, 0, 0);

    return deadlineDate < now;
});

// Check if status should be locked to overdue
const isStatusLocked = computed(() => {
    return isDeadlinePast.value && formEdit.value.status === "overdue";
});

// Watch deadline changes and auto-set status to overdue
watch(deadline, (newDeadline) => {
    if (newDeadline && isDeadlinePast.value && canEditAll.value) {
        formEdit.value.status = "overdue";
    }
});

// Auto-calculate next_occurrence
const nextOccurrence = computed(() => {
    if (
        formEdit.value.isRecurring !== "true" ||
        !startDate.value ||
        !formEdit.value.frequency
    ) {
        return undefined;
    }

    const start = startDate.value.toDate(getLocalTimeZone());
    let nextDate = new Date(start);

    switch (formEdit.value.frequency) {
        case "daily":
            nextDate.setDate(nextDate.getDate() + 1);
            break;
        case "weekly":
            nextDate.setDate(nextDate.getDate() + 7);
            break;
        case "monthly":
            nextDate.setMonth(nextDate.getMonth() + 1);
            break;
        case "yearly":
            nextDate.setFullYear(nextDate.getFullYear() + 1);
            break;
    }

    return new CalendarDate(
        nextDate.getFullYear(),
        nextDate.getMonth() + 1,
        nextDate.getDate()
    );
});

watch(
    () => [
        formEdit.value.isRecurring,
        startDate.value,
        formEdit.value.frequency
    ],
    () => {
        // Trigger next occurrence recalculation
    }
);

// --- Time Logger Functions (Backend Connected) ---

// Fetch time entries from backend
const fetchTimeEntries = async () => {
    try {
        console.log(`Fetching time entries for task ${taskId.value}`);
        const res = await fetch(
            `${API_BASE_URL}/tasks/${taskId.value}/time-entries`
        );

        if (res.status === 404) {
            console.log("No time entries found (task may not exist yet)");
            timeEntries.value = [];
            return;
        }

        if (!res.ok)
            throw new Error(`Failed to fetch time entries: ${res.statusText}`);

        const data = await res.json();
        timeEntries.value = data.time_entries || [];

        console.log(`✅ Loaded ${timeEntries.value.length} time entries`);
        console.log(timeEntries.value);
    } catch (err: any) {
        console.error("Failed to fetch time entries:", err);
        // Don't show toast for initial load failure - task might not have time entries yet
        timeEntries.value = [];
    }
};

// Add time entry to backend
const addTimeEntry = async () => {
    if (newTimeEntry.value.hours === 0 && newTimeEntry.value.minutes === 0) {
        toast({
            title: "Invalid time",
            description: "Please enter at least 1 minute",
            variant: "destructive"
        });
        return;
    }

    try {
        const currentUserId = userData.value?.user?.id;
        const currentUserName = userData.value?.user?.name || "Unknown User";

        if (!currentUserId) {
            toast({
                title: "Authentication required",
                description: "Unable to log time. Please log in again.",
                variant: "destructive"
            });
            return;
        }

        // ✅ FIX: Match the expected structure
        const payload = {
            entry: {
                hours: newTimeEntry.value.hours,
                minutes: newTimeEntry.value.minutes,
                description: newTimeEntry.value.description
            },
            user_id: currentUserId,
            user_name: currentUserName
        };

        console.log("🚀 Adding time entry with payload:", payload);

        const response = await fetch(
            `${API_BASE_URL}/tasks/${taskId.value}/time-entries`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            }
        );

        if (!response.ok) {
            const errorData = await response
                .json()
                .catch(() => ({ detail: "Failed to add time entry" }));
            console.error("❌ Backend error:", errorData);
            throw new Error(errorData.detail || "Failed to add time entry");
        }

        const result = await response.json();
        console.log("✅ Time entry added successfully:", result);

        // Add the new entry to local state
        const newEntry: TimeEntry = {
            id: result.entry_id || result.id || crypto.randomUUID(),
            hours: newTimeEntry.value.hours,
            minutes: newTimeEntry.value.minutes,
            description: newTimeEntry.value.description,
            date: new Date().toISOString(),
            userId: currentUserId,
            userName: currentUserName
        };

        timeEntries.value.unshift(newEntry); // Add to beginning of array

        // Reset form
        newTimeEntry.value = {
            hours: 0,
            minutes: 0,
            description: ""
        };
        isAddingTime.value = false;

        toast({
            title: "Time logged successfully!"
        });
    } catch (err: any) {
        console.error("❌ Failed to add time entry:", err);
        toast({
            title: "Error logging time",
            description: err.message,
            variant: "destructive"
        });
    }
};

// Remove time entry from backend
const removeTimeEntry = async (id: string) => {
    const currentUserId = userData.value?.user?.id;

    if (!currentUserId) {
        toast({
            title: "Authentication required",
            description: "Unable to remove time entry. Please log in again.",
            variant: "destructive"
        });
        return;
    }

    try {
        console.log(`🗑️ Removing time entry ${id} for user ${currentUserId}`);

        const response = await fetch(
            `${API_BASE_URL}/tasks/${taskId.value}/time-entries/${id}?user_id=${currentUserId}`,
            {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            }
        );
        if (response.status === 403) {
            toast({
                title: "Access denied",
                description: "You can only delete your own time entries",
                variant: "destructive"
            });
            return;
        }

        if (!response.ok) {
            const errorData = await response
                .json()
                .catch(() => ({ detail: "Failed to remove time entry" }));
            console.error("❌ Backend error:", errorData);
            console.error(
                "❌ Error details:",
                JSON.stringify(errorData, null, 2)
            ); // Add this line
            throw new Error(errorData.detail || "Failed to remove time entry");
        }

        console.log("✅ Time entry removed successfully");

        // Remove from local state
        timeEntries.value = timeEntries.value.filter((e) => e.id !== id);

        toast({
            title: "Time entry removed"
        });
    } catch (err: any) {
        console.error("❌ Failed to remove time entry:", err);
        toast({
            title: "Error removing time entry",
            description: err.message,
            variant: "destructive"
        });
    }
};

const formatTimeEntry = (entry: TimeEntry) => {
    if (entry.hours === 0) return `${entry.minutes}m`;
    if (entry.minutes === 0) return `${entry.hours}h`;
    return `${entry.hours}h ${entry.minutes}m`;
};

const formatEntryDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
};

// --- Fetch All Users ---
const fetchAllUsers = async () => {
    try {
        const res = await fetch("http://localhost:5100/allUsers");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allUsers.value = (data.users || []).map((u: any) => ({
            id: u.id,
            name: u.name || "Unknown User"
        }));
    } catch (err) {
        console.error("Failed to fetch users:", err);
        toast({
            title: "Error loading users",
            description: "Could not load collaborators list",
            variant: "destructive"
        });
    }
};

// --- Fetch Project Tasks for Parent Task Dropdown ---
const fetchProjectTasks = async (projectId: string) => {
    try {
        const res = await fetch(`${COMPOSITE_API_URL}/pid/${projectId}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const tasks = data.project?.tasks || [];
        projectTasks.value = tasks.map((t: any) => ({
            id: t.id,
            name: t.name
        }));
    } catch (err) {
        console.error("Failed to fetch project tasks:", err);
        toast({
            title: "Error loading tasks",
            description: "Could not load parent task options",
            variant: "destructive"
        });
    }
};

// --- Check Authorization ---
const checkAuthorization = () => {
    const currentUserId = userData.value?.user?.id;
    const currentUserRole = userData.value?.user?.role;

    if (!currentUserId) {
        toast({
            title: "Authentication required",
            description:
                "Unable to determine user identity. Please log in again.",
            variant: "destructive"
        });
        return navigateTo("/auth/login");
    }

    if (formEdit.value.createdByUid === currentUserId) {
        canEditAll.value = true;
        canEditCollaborators.value = true;
        console.log("User is creator - full edit access granted");
    } else if (currentUserRole === "manager") {
        canEditAll.value = false;
        canEditCollaborators.value = true;
        console.log("User is manager - collaborator edit access granted");
    } else {
        canEditAll.value = false;
        canEditCollaborators.value = false;
        toast({
            title: "Access Denied",
            description: "You don't have permission to edit this task.",
            variant: "destructive"
        });
        router.push(`/task/${taskId.value}`);
    }
};

// --- Fetch Task Data ---
const fetchTaskData = async () => {
    state.value.loading = true;
    state.value.error = null;
    try {
        const res = await fetch(`${API_BASE_URL}/tasks/${taskId.value}`);
        if (!res.ok)
            throw new Error(`Failed to fetch task details: ${res.statusText}`);
        const data = await res.json();
        const task = data?.task ?? data;

        const scheduleData = data?.schedule?.data ?? data?.schedule ?? {};

        if (!task) throw new Error("Task data not found in response.");

        console.log("Fetched task data:", task);
        console.log("Schedule data:", scheduleData);

        formEdit.value.name = task.name || "";
        formEdit.value.pid = task.pid || "";
        formEdit.value.parentTaskId = task.parentTaskId || "";
        formEdit.value.desc = task.desc || "";
        formEdit.value.notes = task.notes || "";
        formEdit.value.status = task.status || scheduleData.status || "";
        formEdit.value.priorityLabel = task.priorityLabel || "";
        formEdit.value.priorityLevel = task.priorityLevel?.toString() || "";
        formEdit.value.label = task.label || "";
        formEdit.value.createdByUid = task.created_by_uid || "";

        const isRecurring =
            task.is_recurring ?? scheduleData.is_recurring ?? false;
        formEdit.value.isRecurring = isRecurring ? "true" : "false";
        formEdit.value.frequency =
            task.frequency || scheduleData.frequency || "";

        const startISO = task.start || scheduleData.start;
        const deadlineISO = task.deadline || scheduleData.deadline;

        console.log("Start ISO:", startISO, "Deadline ISO:", deadlineISO);

        // Parse dates
        startDate.value = startISO
            ? parseDate(startISO.slice(0, 10))
            : undefined;
        deadline.value = deadlineISO
            ? parseDate(deadlineISO.slice(0, 10))
            : undefined;

        // Extract time from ISO strings (format: YYYY-MM-DDTHH:MM:SS+08:00 or similar)
        if (startISO) {
            try {
                // Parse ISO string and convert to UTC+8 (Singapore time) for display
                const date = new Date(startISO);
                // Use toLocaleString to get time in UTC+8 timezone
                const timeStr = date.toLocaleString("en-GB", {
                    timeZone: "Asia/Singapore",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false
                });
                startTime.value = timeStr;
            } catch (e) {
                console.error("Error parsing start time:", e);
                // Fallback: try to extract time directly from ISO string
                const timeMatch = startISO.match(/T(\d{2}):(\d{2})/);
                if (timeMatch) {
                    startTime.value = `${timeMatch[1]}:${timeMatch[2]}`;
                } else {
                    startTime.value = "09:00";
                }
            }
        }

        if (deadlineISO) {
            try {
                // Parse ISO string and convert to UTC+8 (Singapore time) for display
                const date = new Date(deadlineISO);
                // Use toLocaleString to get time in UTC+8 timezone
                const timeStr = date.toLocaleString("en-GB", {
                    timeZone: "Asia/Singapore",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false
                });
                deadlineTime.value = timeStr;
            } catch (e) {
                console.error("Error parsing deadline time:", e);
                // Fallback: try to extract time directly from ISO string
                const timeMatch = deadlineISO.match(/T(\d{2}):(\d{2})/);
                if (timeMatch) {
                    deadlineTime.value = `${timeMatch[1]}:${timeMatch[2]}`;
                } else {
                    deadlineTime.value = "17:00";
                }
            }
        }

        // Auto-set status to overdue if deadline is in the past
        if (deadline.value && canEditAll.value) {
            const deadlineDate = deadline.value.toDate(getLocalTimeZone());
            const now = new Date();
            deadlineDate.setHours(0, 0, 0, 0);
            now.setHours(0, 0, 0, 0);

            if (deadlineDate < now) {
                formEdit.value.status = "overdue";
            }
        }

        if (Array.isArray(task.collaborators)) {
            const collaboratorIds = task.collaborators
                .map((c: any) => (typeof c === "string" ? c : c?.id))
                .filter(Boolean);

            selectedCollaborators.value = collaboratorIds;
            formEdit.value.collaboratorsCsv = collaboratorIds.join(", ");
        }

        if (formEdit.value.pid) {
            await fetchProjectTasks(formEdit.value.pid);
        }

        checkAuthorization();
    } catch (err: any) {
        state.value.error = err.message;
    } finally {
        state.value.loading = false;
    }
};

// --- Update Task ---
const updateTask = async () => {
    if (!formEdit.value.name.trim()) {
        toast({ title: "Task name is required", variant: "destructive" });
        return;
    }

    if (!isDateRangeValid.value) {
        toast({
            title: "Invalid date range",
            description: "Start date must be before the deadline",
            variant: "destructive"
        });
        return;
    }

    try {
        state.value.saving = true;

        const collaborators = formEdit.value.collaboratorsCsv
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);

        const payload: any = {};

        if (canEditAll.value) {
            payload.name = formEdit.value.name;
            payload.desc = formEdit.value.desc || undefined;
            payload.notes = formEdit.value.notes || undefined;
            payload.priorityLabel = formEdit.value.priorityLabel || undefined;
            payload.priorityLevel = formEdit.value.priorityLevel
                ? parseInt(formEdit.value.priorityLevel)
                : undefined;
            payload.label = formEdit.value.label || undefined;
            payload.status = formEdit.value.status || undefined;
            payload.parentTaskId = formEdit.value.parentTaskId || undefined;
            payload.collaborators =
                collaborators.length > 0 ? collaborators : undefined;

            // Combine date and time for start, defaulting to UTC+8 (Singapore time)
            if (startDate.value) {
                const startDateObj = startDate.value.toDate(getLocalTimeZone());
                const year = startDateObj.getFullYear();
                const month = String(startDateObj.getMonth() + 1).padStart(
                    2,
                    "0"
                );
                const day = String(startDateObj.getDate()).padStart(2, "0");
                const timeStr = startTime.value || "09:00";

                // Create ISO string with UTC+8 offset
                payload.start = `${year}-${month}-${day}T${timeStr}:00+08:00`;
            }

            // Combine date and time for deadline, defaulting to UTC+8 (Singapore time)
            if (deadline.value) {
                const deadlineDateObj = deadline.value.toDate(
                    getLocalTimeZone()
                );
                const year = deadlineDateObj.getFullYear();
                const month = String(deadlineDateObj.getMonth() + 1).padStart(
                    2,
                    "0"
                );
                const day = String(deadlineDateObj.getDate()).padStart(2, "0");
                const timeStr = deadlineTime.value || "17:00";

                // Create ISO string with UTC+8 offset
                payload.deadline = `${year}-${month}-${day}T${timeStr}:00+08:00`;
            }

            payload.is_recurring = formEdit.value.isRecurring === "true";
            if (!payload.is_recurring) {
                payload.frequency = null;
                payload.next_occurrence = null;
            }

            if (formEdit.value.isRecurring === "true") {
                payload.frequency = formEdit.value.frequency || undefined;

                if (nextOccurrence.value) {
                    payload.next_occurrence = nextOccurrence.value
                        .toDate(getLocalTimeZone())
                        .toISOString();
                }
            }
        } else if (canEditCollaborators.value) {
            payload.collaborators =
                collaborators.length > 0 ? collaborators : undefined;
        }

        console.log("Sending payload:", payload);

        const response = await fetch(`${API_BASE_URL}/${taskId.value}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response
                .json()
                .catch(() => ({ detail: "Failed to update task" }));
            throw new Error(errorData.detail || "Failed to update task");
        }

        // toast({ title: "Task updated successfully!" });
        router.push(`/task/${taskId.value}`);
    } catch (err: any) {
        toast({
            title: "Error updating task",
            description: err.message,
            variant: "destructive"
        });
    } finally {
        state.value.saving = false;
    }
};

onMounted(async () => {
    await fetchAllUsers();
    await fetchTaskData();
    await fetchTimeEntries(); // ✅ Load time entries on mount
});
</script>

<template>
    <div class="min-h-screen bg-background">
        <div
            class="container max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 lg:py-12">
            <Button
                variant="ghost"
                @click="handleBack"
                class="mb-6 -ml-2"
                :disabled="state.saving">
                <ArrowLeft class="h-4 w-4 mr-2" /> Back
            </Button>

            <Card>
                <CardHeader>
                    <CardTitle class="text-2xl sm:text-3xl"
                        >Edit Task</CardTitle
                    >
                    <CardDescription>
                        {{
                            canEditAll
                                ? "Update the details for your task"
                                : canEditCollaborators
                                ? "Update collaborators for this task"
                                : "View task details"
                        }}
                    </CardDescription>
                </CardHeader>

                <CardContent class="pt-6">
                    <div
                        v-if="state.loading"
                        class="flex justify-center items-center h-48">
                        <Loader2
                            class="h-8 w-8 animate-spin text-muted-foreground" />
                    </div>

                    <Alert v-else-if="state.error" variant="destructive">
                        <TriangleAlert class="h-4 w-4" />
                        <AlertTitle>Error Loading Task</AlertTitle>
                        <AlertDescription>{{ state.error }}</AlertDescription>
                    </Alert>

                    <form v-else @submit.prevent="updateTask" class="space-y-6">
                        <!-- Authorization Info Alert -->
                        <Alert
                            v-if="canEditCollaborators && !canEditAll"
                            class="border-blue-500 bg-blue-50 dark:bg-blue-950">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-4 w-4"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <AlertTitle>Limited Edit Access</AlertTitle>
                            <AlertDescription
                                >As a manager, you can only modify collaborators
                                for this task.</AlertDescription
                            >
                        </Alert>

                        <!-- Time Logger Section -->
                        <Card class="border-2 shadow-sm">
                            <CardHeader class="pb-4">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="p-2 bg-primary/10 rounded-lg">
                                            <Timer
                                                class="h-5 w-5 text-primary" />
                                        </div>
                                        <div>
                                            <CardTitle class="text-xl"
                                                >Time Tracking</CardTitle
                                            >
                                            <CardDescription
                                                class="text-sm mt-1">
                                                Log time spent working on this
                                                task
                                            </CardDescription>
                                        </div>
                                    </div>
                                    <div class="text-right">
                                        <div
                                            class="text-2xl font-bold text-primary">
                                            {{ formattedTotalTime }}
                                        </div>
                                        <div
                                            class="text-xs text-muted-foreground">
                                            Total logged
                                        </div>
                                    </div>
                                </div>
                            </CardHeader>

                            <CardContent class="space-y-4">
                                <!-- Add Time Entry Form -->
                                <div
                                    v-if="isAddingTime"
                                    class="p-4 border-2 border-dashed rounded-lg space-y-4 bg-muted/30">
                                    <div class="grid gap-4 sm:grid-cols-2">
                                        <div class="space-y-2">
                                            <Label
                                                for="time-hours"
                                                class="text-sm font-medium"
                                                >Hours</Label
                                            >
                                            <Input
                                                id="time-hours"
                                                v-model.number="
                                                    newTimeEntry.hours
                                                "
                                                type="number"
                                                min="0"
                                                max="999"
                                                placeholder="0"
                                                class="text-center text-lg font-medium" />
                                        </div>
                                        <div class="space-y-2">
                                            <Label
                                                for="time-minutes"
                                                class="text-sm font-medium"
                                                >Minutes</Label
                                            >
                                            <Input
                                                id="time-minutes"
                                                v-model.number="
                                                    newTimeEntry.minutes
                                                "
                                                type="number"
                                                min="0"
                                                max="59"
                                                placeholder="0"
                                                class="text-center text-lg font-medium" />
                                        </div>
                                    </div>

                                    <div class="flex gap-2">
                                        <Button
                                            type="button"
                                            @click="addTimeEntry"
                                            class="flex-1"
                                            size="sm">
                                            <Plus class="h-4 w-4 mr-2" />
                                            Log Time
                                        </Button>
                                        <Button
                                            type="button"
                                            variant="outline"
                                            @click="isAddingTime = false"
                                            size="sm">
                                            Cancel
                                        </Button>
                                    </div>
                                </div>

                                <!-- Add Time Button -->
                                <Button
                                    v-else
                                    type="button"
                                    variant="outline"
                                    @click="isAddingTime = true"
                                    class="w-full border-dashed">
                                    <Plus class="h-4 w-4 mr-2" />
                                    Add Time Entry
                                </Button>

                                <!-- Time Entries List -->
                                <div
                                    v-if="timeEntries.length > 0"
                                    class="space-y-2">
                                    <Separator class="my-4" />
                                    <div
                                        class="space-y-2 max-h-80 overflow-y-auto">
                                        <div
                                            v-for="entry in timeEntries"
                                            :key="entry.id"
                                            class="group flex items-start justify-between p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors">
                                            <div class="flex-1 min-w-0">
                                                <div
                                                    class="flex items-center gap-2 mb-1">
                                                    <Badge
                                                        variant="secondary"
                                                        class="font-mono">
                                                        <Clock
                                                            class="h-3 w-3 mr-1" />
                                                        {{
                                                            formatTimeEntry(
                                                                entry
                                                            )
                                                        }}
                                                    </Badge>
                                                    <span
                                                        class="text-xs text-muted-foreground">
                                                        {{
                                                            formatEntryDate(
                                                                entry.date
                                                            )
                                                        }}
                                                    </span>
                                                </div>
                                                <p
                                                    v-if="entry.description"
                                                    class="text-sm text-muted-foreground truncate">
                                                    {{ entry.description }}
                                                </p>
                                                <p
                                                    class="text-xs text-muted-foreground mt-1">
                                                    by {{ entry.userName }}
                                                </p>
                                            </div>
                                            <Button
                                                type="button"
                                                variant="ghost"
                                                size="icon"
                                                class="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
                                                @click="
                                                    removeTimeEntry(entry.id)
                                                ">
                                                <X class="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                </div>

                                <div
                                    v-else-if="!isAddingTime"
                                    class="text-center py-8 text-muted-foreground">
                                    <Clock
                                        class="h-12 w-12 mx-auto mb-3 opacity-20" />
                                    <p class="text-sm">No time entries yet</p>
                                    <p class="text-xs mt-1">
                                        Click "Add Time Entry" to start tracking
                                    </p>
                                </div>
                            </CardContent>
                        </Card>

                        <Separator />

                        <!-- Task Information Section -->
                        <div class="space-y-4">
                            <h3 class="text-lg font-semibold">
                                Task Information
                            </h3>
                            <div class="grid gap-4 sm:gap-6">
                                <div class="space-y-2">
                                    <Label
                                        for="task-name"
                                        class="text-sm font-medium">
                                        Task Name
                                        <span class="text-destructive">*</span>
                                    </Label>
                                    <Input
                                        id="task-name"
                                        v-model="formEdit.name"
                                        placeholder="Enter a descriptive task name"
                                        required
                                        class="w-full"
                                        :disabled="!canEditAll" />
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <Label
                                            for="task-pid"
                                            class="text-sm font-medium"
                                            >Project ID</Label
                                        >
                                        <Input
                                            id="task-pid"
                                            v-model="formEdit.pid"
                                            class="w-full"
                                            disabled />
                                    </div>
                                    <div class="space-y-2">
                                        <Label
                                            for="task-parent"
                                            class="text-sm font-medium"
                                            >Parent Task</Label
                                        >
                                        <Popover
                                            v-model:open="
                                                isParentTaskPopoverOpen
                                            ">
                                            <PopoverTrigger as-child>
                                                <Button
                                                    variant="outline"
                                                    role="combobox"
                                                    class="w-full justify-between"
                                                    :disabled="!canEditAll"
                                                    id="parent-task-trigger">
                                                    <span class="truncate">
                                                        {{
                                                            formEdit.parentTaskId
                                                                ? getTaskName(
                                                                      formEdit.parentTaskId
                                                                  )
                                                                : "Select parent task (optional)"
                                                        }}
                                                    </span>
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        class="ml-2 h-4 w-4 shrink-0 opacity-50"
                                                        viewBox="0 0 24 24"
                                                        fill="none"
                                                        stroke="currentColor">
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M19 9l-7 7-7-7" />
                                                    </svg>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="p-0"
                                                :align="'start'"
                                                :side-offset="4"
                                                as-child>
                                                <div
                                                    class="w-[var(--radix-popper-anchor-width)] p-2">
                                                    <Input
                                                        v-model="
                                                            parentTaskSearchQuery
                                                        "
                                                        placeholder="Search tasks..."
                                                        class="mb-2" />
                                                    <div
                                                        class="max-h-48 overflow-auto">
                                                        <button
                                                            v-if="
                                                                formEdit.parentTaskId
                                                            "
                                                            type="button"
                                                            class="w-full text-left px-3 py-2 text-sm hover:bg-accent rounded-sm transition-colors text-destructive"
                                                            @click="
                                                                clearParentTask
                                                            ">
                                                            Clear parent task
                                                        </button>
                                                        <button
                                                            v-for="task in filteredTasks"
                                                            :key="task.id"
                                                            type="button"
                                                            class="w-full text-left px-3 py-2 text-sm hover:bg-accent rounded-sm transition-colors"
                                                            :class="{
                                                                'bg-accent':
                                                                    formEdit.parentTaskId ===
                                                                    task.id
                                                            }"
                                                            @click="
                                                                selectParentTask(
                                                                    task.id
                                                                )
                                                            ">
                                                            {{ task.name }}
                                                            <span
                                                                v-if="
                                                                    formEdit.parentTaskId ===
                                                                    task.id
                                                                "
                                                                class="ml-2 text-xs text-muted-foreground">
                                                                ✓
                                                            </span>
                                                        </button>
                                                        <div
                                                            v-if="
                                                                filteredTasks.length ===
                                                                0
                                                            "
                                                            class="px-3 py-2 text-sm text-muted-foreground">
                                                            No tasks found
                                                        </div>
                                                    </div>
                                                </div>
                                            </PopoverContent>
                                        </Popover>
                                    </div>
                                </div>

                                <div class="space-y-2">
                                    <Label
                                        for="task-description"
                                        class="text-sm font-medium"
                                        >Description</Label
                                    >
                                    <Textarea
                                        id="task-description"
                                        v-model="formEdit.desc"
                                        placeholder="Describe the task purpose, requirements, and any important details..."
                                        class="resize-none min-h-[100px] w-full"
                                        rows="4"
                                        :disabled="!canEditAll" />
                                </div>

                                <div class="space-y-2">
                                    <Label
                                        for="task-notes"
                                        class="text-sm font-medium"
                                        >Additional Notes</Label
                                    >
                                    <Input
                                        id="task-notes"
                                        v-model="formEdit.notes"
                                        placeholder="Any extra information or reminders"
                                        class="w-full"
                                        :disabled="!canEditAll" />
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <div class="flex items-center gap-2">
                                            <Label
                                                for="task-priority-level"
                                                class="text-sm font-medium"
                                                >Priority Level (1-10)</Label
                                            >
                                            <Popover>
                                                <PopoverTrigger as-child>
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        class="h-5 w-5 rounded-full p-0"
                                                        type="button">
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            class="h-4 w-4 text-muted-foreground"
                                                            fill="none"
                                                            viewBox="0 0 24 24"
                                                            stroke="currentColor">
                                                            <path
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                                stroke-width="2"
                                                                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                        </svg>
                                                    </Button>
                                                </PopoverTrigger>
                                                <PopoverContent
                                                    class="w-auto p-3 text-sm"
                                                    :align="'start'">
                                                    <p
                                                        class="font-semibold mb-1">
                                                        Priority Scale
                                                    </p>
                                                    <p
                                                        class="text-muted-foreground">
                                                        1 = Lowest priority
                                                    </p>
                                                    <p
                                                        class="text-muted-foreground">
                                                        10 = Highest priority
                                                    </p>
                                                </PopoverContent>
                                            </Popover>
                                        </div>
                                        <Input
                                            id="task-priority-level"
                                            v-model="formEdit.priorityLevel"
                                            type="number"
                                            min="1"
                                            max="10"
                                            placeholder="1-10"
                                            class="w-full"
                                            :disabled="!canEditAll" />
                                    </div>

                                    <div class="space-y-2">
                                        <Label
                                            for="task-label"
                                            class="text-sm font-medium"
                                            >Label</Label
                                        >
                                        <Select
                                            v-model="formEdit.label"
                                            :disabled="!canEditAll">
                                            <SelectTrigger
                                                id="task-label"
                                                class="w-full">
                                                <SelectValue
                                                    placeholder="Select label" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="bug"
                                                    >Bug</SelectItem
                                                >
                                                <SelectItem value="feature"
                                                    >Feature</SelectItem
                                                >
                                                <SelectItem value="enhancement"
                                                    >Enhancement</SelectItem
                                                >
                                                <SelectItem
                                                    value="documentation"
                                                    >Documentation</SelectItem
                                                >
                                                <SelectItem value="maintenance"
                                                    >Maintenance</SelectItem
                                                >
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>

                                <!-- Collaborators Combobox -->
                                <div class="space-y-2">
                                    <Label
                                        for="task-collaborators"
                                        class="text-sm font-medium"
                                        >Collaborators</Label
                                    >
                                    <Popover
                                        v-model:open="
                                            isCollaboratorPopoverOpen
                                        ">
                                        <PopoverTrigger as-child>
                                            <Button
                                                variant="outline"
                                                role="combobox"
                                                class="w-full justify-between"
                                                :disabled="
                                                    !canEditCollaborators
                                                "
                                                id="collaborators-trigger">
                                                Search and select collaborators
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    class="ml-2 h-4 w-4 shrink-0 opacity-50"
                                                    viewBox="0 0 24 24"
                                                    fill="none"
                                                    stroke="currentColor">
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        stroke-width="2"
                                                        d="M19 9l-7 7-7-7" />
                                                </svg>
                                            </Button>
                                        </PopoverTrigger>
                                        <PopoverContent
                                            class="p-0"
                                            :align="'start'"
                                            :side-offset="4"
                                            as-child>
                                            <div
                                                class="w-[var(--radix-popper-anchor-width)] p-2">
                                                <Input
                                                    v-model="searchQuery"
                                                    placeholder="Type to search..."
                                                    class="mb-2" />
                                                <div
                                                    class="max-h-48 overflow-auto">
                                                    <button
                                                        v-for="user in filteredUsers"
                                                        :key="user.id"
                                                        type="button"
                                                        class="w-full text-left px-3 py-2 text-sm hover:bg-accent rounded-sm transition-colors"
                                                        :class="{
                                                            'bg-accent':
                                                                selectedCollaborators.includes(
                                                                    user.id
                                                                )
                                                        }"
                                                        @click="
                                                            selectUser(user.id)
                                                        ">
                                                        {{ user.name }}
                                                        <span
                                                            v-if="
                                                                selectedCollaborators.includes(
                                                                    user.id
                                                                )
                                                            "
                                                            class="ml-2 text-xs text-muted-foreground">
                                                            ✓
                                                        </span>
                                                    </button>
                                                    <div
                                                        v-if="
                                                            filteredUsers.length ===
                                                            0
                                                        "
                                                        class="px-3 py-2 text-sm text-muted-foreground">
                                                        No users found
                                                    </div>
                                                </div>
                                            </div>
                                        </PopoverContent>
                                    </Popover>

                                    <!-- Tag Display -->
                                    <div
                                        class="flex flex-wrap gap-2 mt-2"
                                        v-if="selectedCollaborators.length > 0">
                                        <span
                                            v-for="id in selectedCollaborators"
                                            :key="id"
                                            class="px-2 py-1 bg-secondary text-sm rounded-full flex items-center gap-1">
                                            {{ getUserName(id) }}
                                            <button
                                                v-if="canEditCollaborators"
                                                type="button"
                                                @click="removeCollaborator(id)"
                                                class="text-muted-foreground hover:text-destructive">
                                                ✕
                                            </button>
                                        </span>
                                    </div>

                                    <Input
                                        v-model="formEdit.collaboratorsCsv"
                                        type="hidden" />
                                </div>
                            </div>
                        </div>

                        <Separator />

                        <!-- Schedule & Timeline Section -->
                        <div class="space-y-4">
                            <h3 class="text-lg font-semibold">
                                Schedule & Timeline
                            </h3>
                            <div class="grid gap-4">
                                <div class="space-y-2">
                                    <Label
                                        for="task-status"
                                        class="text-sm font-medium">
                                        Status
                                        <span
                                            v-if="isStatusLocked"
                                            class="text-xs text-muted-foreground ml-2"
                                            >(Auto-set to Overdue)</span
                                        >
                                    </Label>
                                    <Select
                                        v-model="formEdit.status"
                                        :disabled="
                                            !canEditAll || isStatusLocked
                                        ">
                                        <SelectTrigger
                                            id="task-status"
                                            class="w-full">
                                            <SelectValue
                                                placeholder="Select status" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="to do"
                                                >To Do</SelectItem
                                            >
                                            <SelectItem value="ongoing"
                                                >Ongoing</SelectItem
                                            >
                                            <SelectItem value="blocked"
                                                >Blocked</SelectItem
                                            >
                                            <SelectItem value="overdue"
                                                >Overdue</SelectItem
                                            >
                                            <SelectItem value="done"
                                                >Done</SelectItem
                                            >
                                        </SelectContent>
                                    </Select>
                                    <p
                                        v-if="isStatusLocked"
                                        class="text-xs text-muted-foreground">
                                        Status is locked to "Overdue" because
                                        the deadline is in the past.
                                    </p>
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <Label
                                            for="task-start"
                                            class="text-sm font-medium"
                                            >Start Date</Label
                                        >
                                        <Popover>
                                            <PopoverTrigger as-child>
                                                <Button
                                                    variant="outline"
                                                    class="w-full justify-start text-left font-normal"
                                                    :class="{
                                                        'border-destructive':
                                                            !isDateRangeValid
                                                    }"
                                                    :disabled="!canEditAll"
                                                    id="task-start">
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        class="h-4 w-4 mr-2"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor">
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                    </svg>
                                                    <span
                                                        class="flex-1 truncate">
                                                        {{
                                                            formatDate(
                                                                startDate
                                                            )
                                                        }}
                                                    </span>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="w-auto p-0"
                                                :align="'start'">
                                                <Calendar
                                                    v-model="startDate"
                                                    :initial-focus="true" />
                                            </PopoverContent>
                                        </Popover>
                                        <!-- Start Time Input -->
                                        <div class="mt-2">
                                            <Label
                                                for="task-start-time"
                                                class="text-xs text-muted-foreground">
                                                Start Time (UTC+8)
                                            </Label>
                                            <Input
                                                id="task-start-time"
                                                v-model="startTime"
                                                type="time"
                                                class="w-full mt-1"
                                                :disabled="!canEditAll"
                                                placeholder="09:00" />
                                        </div>
                                    </div>

                                    <div class="space-y-2">
                                        <Label
                                            for="task-deadline"
                                            class="text-sm font-medium"
                                            >Deadline</Label
                                        >
                                        <Popover>
                                            <PopoverTrigger as-child>
                                                <Button
                                                    variant="outline"
                                                    class="w-full justify-start text-left font-normal"
                                                    :class="{
                                                        'border-destructive':
                                                            !isDateRangeValid
                                                    }"
                                                    :disabled="!canEditAll"
                                                    id="task-deadline">
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        class="h-4 w-4 mr-2"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor">
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                    </svg>
                                                    <span
                                                        class="flex-1 truncate">
                                                        {{
                                                            formatDate(deadline)
                                                        }}
                                                    </span>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="w-auto p-0"
                                                :align="'start'">
                                                <Calendar
                                                    v-model="deadline"
                                                    :initial-focus="true" />
                                            </PopoverContent>
                                        </Popover>
                                        <!-- Deadline Time Input -->
                                        <div class="mt-2">
                                            <Label
                                                for="task-deadline-time"
                                                class="text-xs text-muted-foreground">
                                                Deadline Time (UTC+8)
                                            </Label>
                                            <Input
                                                id="task-deadline-time"
                                                v-model="deadlineTime"
                                                type="time"
                                                class="w-full mt-1"
                                                :disabled="!canEditAll"
                                                placeholder="17:00" />
                                        </div>
                                    </div>
                                </div>

                                <!-- Date validation warning -->
                                <div
                                    v-if="!isDateRangeValid"
                                    class="p-3 bg-destructive/10 border border-destructive rounded-md">
                                    <p class="text-sm text-destructive">
                                        ⚠️ Start date must be before the
                                        deadline
                                    </p>
                                </div>

                                <!-- Recurring Task Section -->
                                <div class="space-y-4 p-4 border rounded-lg">
                                    <div class="space-y-2">
                                        <Label
                                            for="task-recurring"
                                            class="text-sm font-medium"
                                            >Is Recurring Task?</Label
                                        >
                                        <Select
                                            v-model="formEdit.isRecurring"
                                            :disabled="!canEditAll">
                                            <SelectTrigger
                                                id="task-recurring"
                                                class="w-full">
                                                <SelectValue
                                                    placeholder="Select option" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="true"
                                                    >Yes (Recurring)</SelectItem
                                                >
                                                <SelectItem value="false"
                                                    >No (One-time)</SelectItem
                                                >
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div
                                        v-if="formEdit.isRecurring === 'true'"
                                        class="space-y-4 pt-2">
                                        <div class="space-y-2">
                                            <Label
                                                for="task-frequency"
                                                class="text-sm font-medium"
                                                >Frequency</Label
                                            >
                                            <Select
                                                v-model="formEdit.frequency"
                                                :disabled="!canEditAll">
                                                <SelectTrigger
                                                    id="task-frequency"
                                                    class="w-full">
                                                    <SelectValue
                                                        placeholder="Select frequency" />
                                                </SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="daily"
                                                        >Daily</SelectItem
                                                    >
                                                    <SelectItem value="weekly"
                                                        >Weekly</SelectItem
                                                    >
                                                    <SelectItem value="monthly"
                                                        >Monthly</SelectItem
                                                    >
                                                    <SelectItem value="yearly"
                                                        >Yearly</SelectItem
                                                    >
                                                </SelectContent>
                                            </Select>
                                        </div>

                                        <!-- Display auto-calculated next occurrence -->
                                        <div
                                            v-if="nextOccurrence"
                                            class="p-3 bg-muted rounded-md">
                                            <p class="text-sm font-medium mb-1">
                                                Next Occurrence
                                                (Auto-calculated)
                                            </p>
                                            <p
                                                class="text-sm text-muted-foreground">
                                                {{ formatDate(nextOccurrence) }}
                                            </p>
                                            <p
                                                class="text-xs text-muted-foreground mt-1">
                                                Based on start date and
                                                {{ formEdit.frequency }}
                                                frequency
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <Separator />

                        <!-- Action Buttons -->
                        <div
                            class="flex flex-col-reverse sm:flex-row sm:justify-end gap-3 pt-2">
                            <Button
                                variant="outline"
                                type="button"
                                @click="handleBack"
                                class="w-full sm:w-auto"
                                :disabled="state.saving">
                                Cancel
                            </Button>
                            <Button
                                type="submit"
                                :disabled="
                                    state.saving ||
                                    (!canEditAll && !canEditCollaborators)
                                "
                                class="w-full sm:w-auto">
                                <Loader2
                                    v-if="state.saving"
                                    class="h-4 w-4 mr-2 animate-spin" />
                                <span v-if="state.saving"
                                    >Saving Changes...</span
                                >
                                <span v-else>Save Changes</span>
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    </div>
</template>
