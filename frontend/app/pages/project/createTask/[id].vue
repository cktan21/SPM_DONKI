<script setup lang="ts">
import { ref, watch, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import type { DateValue } from "@internationalized/date";
import { getLocalTimeZone, CalendarDate } from "@internationalized/date";

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

const router = useRouter();
const route = useRoute();
const { toast } = useToast();

const API_BASE_URL = "http://localhost:4000";

// Get authenticated user data from middleware
const userData = useState<any>("userData");

const formCreate = ref({
    name: "",
    pid: "",
    parentTaskId: "",
    collaboratorsCsv: "",
    desc: "",
    notes: "",
    priorityLevel: "",
    label: "",
    isRecurring: "false", // String "true" or "false"
    schedule: {
        status: "",
        start: undefined as DateValue | undefined,
        deadline: undefined as DateValue | undefined,
        frequency: ""
    }
});

onMounted(() => {
    formCreate.value.pid = route.params.id as string;
    fetchAllUsers();
});

const state = ref({ creating: false });
const handleBack = () => router.back();

// Helper function to format date as dd/mm/yyyy
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

// Computed property to check if dates are valid (start must be before deadline)
const isDateRangeValid = computed(() => {
    if (
        !formCreate.value.schedule.start ||
        !formCreate.value.schedule.deadline
    ) {
        return true; // If either date is missing, don't show error
    }

    const startDate = formCreate.value.schedule.start.toDate(
        getLocalTimeZone()
    );
    const deadlineDate = formCreate.value.schedule.deadline.toDate(
        getLocalTimeZone()
    );

    return startDate < deadlineDate;
});

// Computed property to auto-calculate next_occurrence based on start date and frequency
const nextOccurrence = computed(() => {
    if (
        formCreate.value.isRecurring !== "true" ||
        !formCreate.value.schedule.start ||
        !formCreate.value.schedule.frequency
    ) {
        return undefined;
    }

    const startDate = formCreate.value.schedule.start.toDate(
        getLocalTimeZone()
    );
    let nextDate = new Date(startDate);

    switch (formCreate.value.schedule.frequency) {
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

// Watch for changes in recurring settings
watch(
    () => [
        formCreate.value.isRecurring,
        formCreate.value.schedule.start,
        formCreate.value.schedule.frequency
    ],
    () => {
        // This will trigger the computed property to recalculate
    }
);

const selectedCollaborator = ref("");
const selectedCollaborators = ref<string[]>([]);
const allUsers = ref<{ id: string; name: string }[]>([]);
const isCollaboratorPopoverOpen = ref(false);

const getUserName = (id: string) =>
    allUsers.value.find((u) => u.id === id)?.name || id;

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

const removeCollaborator = (id: string) => {
    selectedCollaborators.value = selectedCollaborators.value.filter(
        (x) => x !== id
    );
    formCreate.value.collaboratorsCsv = selectedCollaborators.value.join(", ");
};

const searchQuery = ref("");

const filteredUsers = computed(() =>
    allUsers.value.filter((u) =>
        u.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
);

const selectUser = (id: string) => {
    if (!selectedCollaborators.value.includes(id)) {
        selectedCollaborators.value.push(id);
        formCreate.value.collaboratorsCsv =
            selectedCollaborators.value.join(", ");
    }
    // Close popover and reset search
    isCollaboratorPopoverOpen.value = false;
    searchQuery.value = "";
};

const createTask = async () => {
    if (!formCreate.value.name.trim()) {
        toast({ title: "Task name is required", variant: "destructive" });
        return;
    }

    // Validate date range
    if (!isDateRangeValid.value) {
        toast({
            title: "Invalid date range",
            description: "Start date must be before the deadline",
            variant: "destructive"
        });
        return;
    }

    // Get created_by_uid from authenticated user
    const createdByUid = userData.value?.user?.id;

    if (!createdByUid) {
        toast({
            title: "Authentication required",
            description:
                "Unable to determine user identity. Please log in again.",
            variant: "destructive"
        });
        return navigateTo("/auth/login");
    }

    try {
        state.value.creating = true;

        const collaborators = formCreate.value.collaboratorsCsv
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);

        const schedule: any = {};

        if (formCreate.value.schedule.status)
            schedule.status = formCreate.value.schedule.status;

        if (formCreate.value.schedule.start)
            schedule.start = formCreate.value.schedule.start
                .toDate(getLocalTimeZone())
                .toISOString();

        if (formCreate.value.schedule.deadline)
            schedule.deadline = formCreate.value.schedule.deadline
                .toDate(getLocalTimeZone())
                .toISOString();

        // Only set is_recurring if we have a deadline (required for schedule)
        // This prevents sending schedule without required fields
        if (formCreate.value.schedule.deadline) {
            // Convert string "true"/"false" to boolean (backend expects boolean)
            schedule.is_recurring = formCreate.value.isRecurring === "true";

            if (formCreate.value.schedule.frequency)
                schedule.frequency = formCreate.value.schedule.frequency;

            // Auto-calculate next_occurrence if recurring is enabled
            if (
                formCreate.value.isRecurring === "true" &&
                nextOccurrence.value
            ) {
                schedule.next_occurrence = nextOccurrence.value
                    .toDate(getLocalTimeZone())
                    .toISOString();
            }
        }

        // Only include schedule if it has at least a deadline (required by backend)
        // If schedule only has is_recurring but no deadline, don't send it
        const scheduleToSend = schedule.deadline ? schedule : undefined;

        const payload: any = {
            name: formCreate.value.name,
            desc: formCreate.value.desc || undefined,
            notes: formCreate.value.notes || undefined,
            pid: formCreate.value.pid || undefined,
            parentTaskId: formCreate.value.parentTaskId || undefined,
            // Only include collaborators if array is not empty
            collaborators: collaborators.length > 0 ? collaborators : undefined,
            priorityLevel: formCreate.value.priorityLevel
                ? parseInt(formCreate.value.priorityLevel)
                : 3,
            label: formCreate.value.label || undefined,
            created_by_uid: createdByUid,
            schedule: scheduleToSend
        };

        console.log(payload);

        const response = await fetch(`${API_BASE_URL}/createTask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error(`Failed: ${response.statusText}`);

        const responseData = await response.json();

        // Get the project ID from the created task response or use the one from form
        const projectId = responseData.task?.pid || formCreate.value.pid;

        toast({ title: "Task created successfully!" });

        // Clear the selected project state to force fresh data fetch
        const selectedProject = useState<any>("selectedProject");
        selectedProject.value = null;

        // Navigate back to the project page with the project ID
        // The project page will detect the missing state and fetch fresh data
        router.push(`/project/${projectId}`);
    } catch (err: any) {
        toast({
            title: "Error creating task",
            description: err.message,
            variant: "destructive"
        });
    } finally {
        state.value.creating = false;
    }
};
</script>

<template>
    <div class="min-h-screen bg-background">
        <div
            class="container max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8 lg:py-12">
            <!-- Back Button -->
            <Button variant="ghost" @click="handleBack" class="mb-6 -ml-2">
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
                        d="M15 19l-7-7 7-7" />
                </svg>
                Back
            </Button>

            <!-- Form Card -->
            <Card>
                <CardHeader>
                    <CardTitle class="text-2xl sm:text-3xl"
                        >Create New Task</CardTitle
                    >
                    <CardDescription>
                        Fill in the details below to create a new task for your
                        project
                    </CardDescription>
                </CardHeader>

                <CardContent class="pt-6">
                    <form @submit.prevent="createTask" class="space-y-6">
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
                                        v-model="formCreate.name"
                                        placeholder="Enter a descriptive task name"
                                        required
                                        class="w-full" />
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <Label
                                            for="task-pid"
                                            class="text-sm font-medium">
                                            Project ID
                                        </Label>
                                        <Input
                                            id="task-pid"
                                            v-model="formCreate.pid"
                                            placeholder="Optional project identifier"
                                            class="w-full"
                                            readonly />
                                    </div>

                                    <div class="space-y-2">
                                        <Label
                                            for="task-parent"
                                            class="text-sm font-medium">
                                            Parent Task ID
                                        </Label>
                                        <Input
                                            id="task-parent"
                                            v-model="formCreate.parentTaskId"
                                            placeholder="Optional parent task"
                                            class="w-full" />
                                    </div>
                                </div>

                                <div class="space-y-2">
                                    <Label
                                        for="task-description"
                                        class="text-sm font-medium">
                                        Description
                                    </Label>
                                    <Textarea
                                        id="task-description"
                                        v-model="formCreate.desc"
                                        placeholder="Describe the task purpose, requirements, and any important details..."
                                        class="resize-none min-h-[100px] w-full"
                                        rows="4" />
                                </div>

                                <div class="space-y-2">
                                    <Label
                                        for="task-notes"
                                        class="text-sm font-medium">
                                        Additional Notes
                                    </Label>
                                    <Input
                                        id="task-notes"
                                        v-model="formCreate.notes"
                                        placeholder="Any extra information or reminders"
                                        class="w-full" />
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <div class="flex items-center gap-2">
                                            <Label
                                                for="task-priority"
                                                class="text-sm font-medium">
                                                Priority Level (1-10)
                                            </Label>
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
                                            id="task-priority"
                                            v-model="formCreate.priorityLevel"
                                            type="number"
                                            min="1"
                                            max="10"
                                            placeholder="1-10"
                                            class="w-full" />
                                    </div>

                                    <div class="space-y-2">
                                        <Label
                                            for="task-label"
                                            class="text-sm font-medium">
                                            Label
                                        </Label>
                                        <Select v-model="formCreate.label">
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
                                                    value="documentation">
                                                    Documentation
                                                </SelectItem>
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
                                        class="text-sm font-medium">
                                        Collaborators
                                    </Label>
                                    <Popover
                                        v-model:open="
                                            isCollaboratorPopoverOpen
                                        ">
                                        <PopoverTrigger as-child>
                                            <Button
                                                variant="outline"
                                                role="combobox"
                                                class="w-full justify-between">
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
                                            class="w-[var(--radix-popover-trigger-width)] p-0"
                                            :align="'start'"
                                            :side-offset="4">
                                            <div class="p-2">
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
                                                type="button"
                                                @click="removeCollaborator(id)"
                                                class="text-muted-foreground hover:text-destructive">
                                                ✕
                                            </button>
                                        </span>
                                    </div>

                                    <Input
                                        v-model="formCreate.collaboratorsCsv"
                                        type="hidden" />
                                </div>
                            </div>
                        </div>

                        <Separator />

                        <!-- Schedule Section -->
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
                                    </Label>
                                    <Select
                                        v-model="formCreate.schedule.status">
                                        <SelectTrigger
                                            id="task-status"
                                            class="w-full">
                                            <SelectValue
                                                placeholder="Select status" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="to do"
                                                >To-do</SelectItem
                                            >
                                            <SelectItem value="ongoing"
                                                >Ongoing</SelectItem
                                            >
                                            <SelectItem value="done"
                                                >Done</SelectItem
                                            >
                                            <SelectItem value="blocked"
                                                >Blocked</SelectItem
                                            >
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div class="grid gap-4 sm:grid-cols-2">
                                    <div class="space-y-2">
                                        <Label
                                            for="task-start"
                                            class="text-sm font-medium">
                                            Start Date
                                        </Label>
                                        <Popover>
                                            <PopoverTrigger as-child>
                                                <Button
                                                    variant="outline"
                                                    class="w-full justify-start text-left font-normal"
                                                    :class="{
                                                        'border-destructive':
                                                            !isDateRangeValid
                                                    }"
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
                                                                formCreate
                                                                    .schedule
                                                                    .start
                                                            )
                                                        }}
                                                    </span>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="w-auto p-0"
                                                :align="'start'">
                                                <Calendar
                                                    :model-value="
                            (formCreate.schedule.start as DateValue | undefined)
                          "
                                                    @update:model-value="
                            (value: DateValue | undefined) =>
                              (formCreate.schedule.start = value)
                          "
                                                    :initial-focus="true" />
                                            </PopoverContent>
                                        </Popover>
                                    </div>

                                    <div class="space-y-2">
                                        <Label
                                            for="task-deadline"
                                            class="text-sm font-medium">
                                            Deadline
                                        </Label>
                                        <Popover>
                                            <PopoverTrigger as-child>
                                                <Button
                                                    variant="outline"
                                                    class="w-full justify-start text-left font-normal"
                                                    :class="{
                                                        'border-destructive':
                                                            !isDateRangeValid
                                                    }"
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
                                                            formatDate(
                                                                formCreate
                                                                    .schedule
                                                                    .deadline
                                                            )
                                                        }}
                                                    </span>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="w-auto p-0"
                                                :align="'start'">
                                                <Calendar
                                                    :model-value="
                            (formCreate.schedule
                              .deadline as DateValue | undefined)
                          "
                                                    @update:model-value="
                            (value: DateValue | undefined) =>
                              (formCreate.schedule.deadline = value)
                          "
                                                    :initial-focus="true" />
                                            </PopoverContent>
                                        </Popover>
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
                                            class="text-sm font-medium">
                                            Is Recurring Task?
                                        </Label>
                                        <Select
                                            v-model="formCreate.isRecurring">
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
                                        v-if="formCreate.isRecurring === 'true'"
                                        class="space-y-4 pt-2">
                                        <div class="space-y-2">
                                            <Label
                                                for="task-frequency"
                                                class="text-sm font-medium">
                                                Frequency
                                            </Label>
                                            <Select
                                                v-model="
                                                    formCreate.schedule
                                                        .frequency
                                                ">
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
                                                {{
                                                    formCreate.schedule
                                                        .frequency
                                                }}
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
                                class="w-full sm:w-auto">
                                Cancel
                            </Button>
                            <Button
                                type="submit"
                                :disabled="state.creating"
                                class="w-full sm:w-auto">
                                <svg
                                    v-if="state.creating"
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-4 w-4 mr-2 animate-spin"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                </svg>
                                <span v-if="state.creating"
                                    >Creating Task...</span
                                >
                                <span v-else>Create Task</span>
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    </div>
</template>
