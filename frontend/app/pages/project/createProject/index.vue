<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

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
    Popover,
    PopoverTrigger,
    PopoverContent
} from "@/components/ui/popover";
import { useToast } from "@/components/ui/toast";

const router = useRouter();
const { toast } = useToast();

const API_BASE_URL = "http://localhost:8000/project";

// Get authenticated user data from middleware
const userData = useState<any>("userData");

const formCreate = ref({
    name: "",
    desc: "",
    membersCsv: ""
});

onMounted(() => {
    fetchAllUsers();
});

const state = ref({ creating: false });
const handleBack = () => router.back();

// Validation state for required fields
const validationErrors = ref({
    name: false
});

// Computed properties for validation
const isNameValid = computed(() => formCreate.value.name.trim().length > 0);

const selectedMember = ref("");
const selectedMembers = ref<string[]>([]);
const allUsers = ref<{ id: string; name: string }[]>([]);
const isMemberPopoverOpen = ref(false);

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
            description: "Could not load members list",
            variant: "destructive"
        });
    }
};

const removeMember = (id: string) => {
    selectedMembers.value = selectedMembers.value.filter((x) => x !== id);
    formCreate.value.membersCsv = selectedMembers.value.join(", ");
};

const searchQuery = ref("");

const filteredUsers = computed(() =>
    allUsers.value.filter((u) =>
        u.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
);

const selectUser = (id: string) => {
    if (!selectedMembers.value.includes(id)) {
        selectedMembers.value.push(id);
        formCreate.value.membersCsv = selectedMembers.value.join(", ");
    }
    // Close popover and reset search
    isMemberPopoverOpen.value = false;
    searchQuery.value = "";
};

const createProject = async () => {
    // Reset validation errors
    validationErrors.value = {
        name: false
    };

    // Validate required fields
    let hasErrors = false;

    if (!isNameValid.value) {
        validationErrors.value.name = true;
        hasErrors = true;
    }

    // If there are validation errors, don't submit
    if (hasErrors) {
        return;
    }

    // Get uid from authenticated user
    const uid = userData.value?.user?.id;

    if (!uid) {
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

        const members = formCreate.value.membersCsv
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean);

        const payload: any = {
            uid: uid,
            name: formCreate.value.name,
            desc: formCreate.value.desc || undefined,
            members: members.length > 0 ? members : []
        };

        console.log(payload);

        const response = await fetch(`${API_BASE_URL}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                errorData.detail || `Failed: ${response.statusText}`
            );
        }

        const responseData = await response.json();

        // Get the project ID from the created project response
        const projectId = responseData.project?.id || responseData.data?.id;

        // Clear the cached projects to force fresh data fetch
        const cachedProjects = useState<any>("dashboardProjects");
        cachedProjects.value = [];

        // Navigate back to the dashboard
        router.push("/dashboard");
    } catch (err: any) {
        toast({
            title: "Error creating project",
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
                        >Create New Project</CardTitle
                    >
                    <CardDescription>
                        Fill in the details below to create a new project
                    </CardDescription>
                </CardHeader>

                <CardContent class="pt-6">
                    <form @submit.prevent="createProject" class="space-y-6">
                        <!-- Project Information Section -->
                        <div class="space-y-4">
                            <h3 class="text-lg font-semibold">
                                Project Information
                            </h3>
                            <div class="grid gap-4 sm:gap-6">
                                <div class="space-y-2">
                                    <div class="flex items-center gap-2">
                                        <Label
                                            for="project-name"
                                            class="text-sm font-medium">
                                            Project Name
                                            <span class="text-destructive"
                                                >*</span
                                            >
                                        </Label>
                                        <Popover
                                            v-model:open="
                                                validationErrors.name
                                            ">
                                            <PopoverTrigger as-child>
                                                <Button
                                                    v-if="validationErrors.name"
                                                    variant="ghost"
                                                    size="icon"
                                                    class="h-5 w-5 rounded-full p-0"
                                                    type="button">
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        class="h-4 w-4 text-destructive"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor">
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            stroke-width="2"
                                                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                    </svg>
                                                </Button>
                                            </PopoverTrigger>
                                            <PopoverContent
                                                class="w-auto p-3 text-sm"
                                                :align="'start'">
                                                <p
                                                    class="font-semibold mb-1 text-destructive">
                                                    Project Name Required
                                                </p>
                                                <p
                                                    class="text-muted-foreground">
                                                    Please enter a project name
                                                    before submitting.
                                                </p>
                                            </PopoverContent>
                                        </Popover>
                                    </div>
                                    <Input
                                        id="project-name"
                                        v-model="formCreate.name"
                                        placeholder="Enter a descriptive project name"
                                        required
                                        :class="[
                                            'w-full',
                                            validationErrors.name
                                                ? 'border-destructive'
                                                : ''
                                        ]"
                                        @input="
                                            validationErrors.name = false
                                        " />
                                </div>

                                <div class="space-y-2">
                                    <Label
                                        for="project-description"
                                        class="text-sm font-medium">
                                        Description
                                    </Label>
                                    <Textarea
                                        id="project-description"
                                        v-model="formCreate.desc"
                                        placeholder="Describe the project purpose, goals, and any important details..."
                                        class="resize-none min-h-[100px] w-full"
                                        rows="4" />
                                </div>

                                <!-- Members Combobox -->
                                <div class="space-y-2">
                                    <Label
                                        for="project-members"
                                        class="text-sm font-medium">
                                        Team Members
                                    </Label>
                                    <Popover v-model:open="isMemberPopoverOpen">
                                        <PopoverTrigger as-child>
                                            <Button
                                                variant="outline"
                                                role="combobox"
                                                class="w-full justify-between">
                                                Search and select team members
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
                                                                selectedMembers.includes(
                                                                    user.id
                                                                )
                                                        }"
                                                        @click="
                                                            selectUser(user.id)
                                                        ">
                                                        {{ user.name }}
                                                        <span
                                                            v-if="
                                                                selectedMembers.includes(
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
                                        v-if="selectedMembers.length > 0">
                                        <span
                                            v-for="id in selectedMembers"
                                            :key="id"
                                            class="px-2 py-1 bg-secondary text-sm rounded-full flex items-center gap-1">
                                            {{ getUserName(id) }}
                                            <button
                                                type="button"
                                                @click="removeMember(id)"
                                                class="text-muted-foreground hover:text-destructive">
                                                ✕
                                            </button>
                                        </span>
                                    </div>

                                    <Input
                                        v-model="formCreate.membersCsv"
                                        type="hidden" />
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
                                    >Creating Project...</span
                                >
                                <span v-else>Create Project</span>
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    </div>
</template>
