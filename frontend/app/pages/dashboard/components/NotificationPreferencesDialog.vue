<script setup lang="ts">
import { computed } from "vue";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import {
    useNotificationPreferences,
    type NotificationEventType
} from "~/composables/useNotificationPreferences";
import { Settings2, CheckSquare, Square } from "lucide-vue-next";

const props = defineProps<{
    open: boolean;
}>();

const emit = defineEmits<{
    "update:open": [value: boolean];
}>();

const {
    preferences,
    toggle,
    enableAll,
    disableAll,
    reset,
    eventTypes,
    enable,
    disable
} = useNotificationPreferences();

// Handler for checkbox updates - receives the new boolean value from the checkbox
const handleCheckboxChange = (
    eventType: NotificationEventType,
    value: boolean
) => {
    if (value) {
        enable(eventType);
    } else {
        disable(eventType);
    }
};

// Human-readable labels for event types
const eventTypeLabels: Record<NotificationEventType, string> = {
    task_created: "Task Created",
    task_updated: "Task Updated",
    task_deleted: "Task Deleted",
    task_assigned: "Task Assigned",
    task_status_changed: "Task Status Changed",
    deadline_approaching: "Deadline Approaching",
    deadline_overdue: "Deadline Overdue",
    recurring_task_reset: "Recurring Task Reset",
    project_created: "Project Created",
    project_collaborator_added: "Added to Project"
};

// Group event types by category
const taskEvents: NotificationEventType[] = [
    "task_created",
    "task_updated",
    "task_deleted",
    "task_assigned",
    "task_status_changed"
];

const deadlineEvents: NotificationEventType[] = [
    "deadline_approaching",
    "deadline_overdue"
];

const recurringEvents: NotificationEventType[] = ["recurring_task_reset"];

const projectEvents: NotificationEventType[] = [
    "project_created",
    "project_collaborator_added"
];

const isOpen = computed({
    get: () => props.open,
    set: (value) => emit("update:open", value)
});

// Computed: Count of enabled notifications
const enabledCount = computed(() => {
    return Object.values(preferences).filter(Boolean).length;
});

// Computed: Check if all are enabled
const allEnabled = computed(() => {
    return enabledCount.value === eventTypes.length;
});

// Computed: Check if all are disabled
const allDisabled = computed(() => {
    return enabledCount.value === 0;
});

// Toggle all notifications
const toggleAll = () => {
    if (allEnabled.value) {
        disableAll();
    } else {
        enableAll();
    }
};
</script>

<template>
    <Dialog v-model:open="isOpen">
        <DialogContent
            class="sm:max-w-[500px] max-h-[80vh] overflow-hidden flex flex-col">
            <DialogHeader>
                <DialogTitle class="flex items-center gap-2">
                    <Settings2 class="h-5 w-5" />
                    Notification Preferences
                </DialogTitle>
                <DialogDescription>
                    Select which notifications you want to receive. All
                    notifications are enabled by default.
                </DialogDescription>
            </DialogHeader>

            <div class="flex-1 overflow-y-auto py-4">
                <!-- Quick Actions -->
                <div
                    class="flex items-center justify-between mb-4 pb-3 border-b">
                    <div class="flex items-center gap-2">
                        <span class="text-sm font-medium">
                            {{ enabledCount }} of
                            {{ eventTypes.length }} enabled
                        </span>
                    </div>
                    <div class="flex items-center gap-2">
                        <Button
                            variant="outline"
                            size="sm"
                            @click="toggleAll"
                            class="h-8 text-xs">
                            <CheckSquare
                                v-if="allEnabled"
                                class="h-3 w-3 mr-1" />
                            <Square v-else class="h-3 w-3 mr-1" />
                            {{ allEnabled ? "Deselect All" : "Select All" }}
                        </Button>
                        <Button
                            variant="ghost"
                            size="sm"
                            @click="reset"
                            class="h-8 text-xs">
                            Reset
                        </Button>
                    </div>
                </div>

                <!-- Task Events -->
                <div class="mb-4">
                    <h3 class="text-sm font-semibold mb-2 text-gray-700">
                        Task Events
                    </h3>
                    <div class="space-y-2">
                        <label
                            v-for="eventType in taskEvents"
                            :key="eventType"
                            class="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                            <Checkbox
                                :model-value="preferences[eventType]"
                                @update:model-value="
                                    (value) =>
                                        handleCheckboxChange(eventType, value)
                                " />
                            <span class="text-sm flex-1">{{
                                eventTypeLabels[eventType]
                            }}</span>
                        </label>
                    </div>
                </div>

                <Separator class="my-4" />

                <!-- Deadline Events -->
                <div class="mb-4">
                    <h3 class="text-sm font-semibold mb-2 text-gray-700">
                        Deadline Events
                    </h3>
                    <div class="space-y-2">
                        <label
                            v-for="eventType in deadlineEvents"
                            :key="eventType"
                            class="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                            <Checkbox
                                :model-value="preferences[eventType]"
                                @update:model-value="
                                    (value) =>
                                        handleCheckboxChange(eventType, value)
                                " />
                            <span class="text-sm flex-1">{{
                                eventTypeLabels[eventType]
                            }}</span>
                        </label>
                    </div>
                </div>

                <Separator class="my-4" />

                <!-- Recurring Events -->
                <div class="mb-4">
                    <h3 class="text-sm font-semibold mb-2 text-gray-700">
                        Recurring Events
                    </h3>
                    <div class="space-y-2">
                        <label
                            v-for="eventType in recurringEvents"
                            :key="eventType"
                            class="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                            <Checkbox
                                :model-value="preferences[eventType]"
                                @update:model-value="
                                    (value) =>
                                        handleCheckboxChange(eventType, value)
                                " />
                            <span class="text-sm flex-1">{{
                                eventTypeLabels[eventType]
                            }}</span>
                        </label>
                    </div>
                </div>

                <Separator class="my-4" />

                <!-- Project Events -->
                <div class="mb-4">
                    <h3 class="text-sm font-semibold mb-2 text-gray-700">
                        Project Events
                    </h3>
                    <div class="space-y-2">
                        <label
                            v-for="eventType in projectEvents"
                            :key="eventType"
                            class="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                            <Checkbox
                                :model-value="preferences[eventType]"
                                @update:model-value="
                                    (value) =>
                                        handleCheckboxChange(eventType, value)
                                " />
                            <span class="text-sm flex-1">{{
                                eventTypeLabels[eventType]
                            }}</span>
                        </label>
                    </div>
                </div>
            </div>

            <DialogFooter>
                <Button variant="outline" @click="isOpen = false">Close</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
