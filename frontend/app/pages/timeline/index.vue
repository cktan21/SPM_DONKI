<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <LoadingState v-if="loading" />
        <ErrorState v-else-if="error" :error="error" @retry="fetchData" />

        <div v-else>
            <TimelineHeader
                :userData="userData"
                :currentView="currentView"
                :viewModes="viewModes"
                :projects="projects"
                :teamMembers="teamMembers"
                :selectedProject="selectedProject"
                :selectedTeamMember="selectedTeamMember"
                :filterStatus="filterStatus"
                :filterPriority="filterPriority"
                :selectedTimeRange="selectedTimeRange"
                :timeRanges="timeRanges"
                @update:currentView="currentView = $event"
                @update:selectedProject="selectedProject = $event"
                @update:selectedTeamMember="selectedTeamMember = $event"
                @update:filterStatus="filterStatus = $event"
                @update:filterPriority="filterPriority = $event"
                @update:selectedTimeRange="selectedTimeRange = $event" />

            <div class="max-w-[1400px] mx-auto px-4 sm:px-6 py-6 sm:py-8">
                <StatsCards :stats="stats" />

                <TimelineContent
                    :currentView="currentView"
                    :filteredTasks="filteredTasks"
                    :filteredTeamMembers="filteredTeamMembers"
                    :selectedTimeRange="selectedTimeRange"
                    @selectTask="selectedTask = $event" />
            </div>
        </div>

        <TaskDetailModal
            v-if="selectedTask"
            :task="selectedTask"
            @close="selectedTask = null" />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import LoadingState from "~/pages/timeline/components/LoadingState.vue";
import ErrorState from "~/pages/timeline/components/ErrorState.vue";
import TimelineHeader from "~/pages/timeline/components/TimelineHeader.vue";
import StatsCards from "~/pages/timeline/components/StatsCards.vue";
import TimelineContent from "~/pages/timeline/components/TimelineContent.vue";
import TaskDetailModal from "~/pages/timeline/components/TaskDetailModal.vue";

// Get user data from middleware
const userDataFromMiddleware = useState("userData");
const userId = computed(() => userDataFromMiddleware.value?.user?.id || null);

const loading = ref(true);
const error = ref(null);
const userData = ref({});
const currentView = ref("personal");
const selectedProject = ref("all");
const selectedTeamMember = ref("all");
const filterStatus = ref("all");
const filterPriority = ref("all");
const selectedTimeRange = ref("month");
const selectedTask = ref(null);
const projects = ref([]);
const allTasks = ref([]);
const teamMembers = ref([]);

const viewModes = [
    { label: "My Schedule", value: "personal" },
    { label: "Team Schedule", value: "team" }
];

const timeRanges = [
    { label: "Week", value: "week" },
    { label: "Month", value: "month" },
    { label: "Quarter", value: "quarter" }
];

const stats = computed(() => {
    const tasks =
        currentView.value === "personal"
            ? filteredTasks.value
            : allTeamTasks.value;
    return {
        total: tasks.length,
        ongoing: tasks.filter((t) => t.status === "ongoing").length,
        overdue: tasks.filter((t) => t.status === "overdue").length,
        done: tasks.filter((t) => t.status === "done").length
    };
});

const filteredTasks = computed(() => {
    let tasks = allTasks.value;

    if (selectedProject.value !== "all") {
        tasks = tasks.filter((t) => t.project.id === selectedProject.value);
    }

    if (filterStatus.value !== "all") {
        tasks = tasks.filter((t) => t.status === filterStatus.value);
    }

    if (filterPriority.value !== "all") {
        if (filterPriority.value === "high") {
            tasks = tasks.filter((t) => t.priorityLevel >= 8);
        } else if (filterPriority.value === "medium") {
            tasks = tasks.filter(
                (t) => t.priorityLevel >= 4 && t.priorityLevel < 8
            );
        } else {
            tasks = tasks.filter((t) => t.priorityLevel < 4);
        }
    }

    return tasks.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
});

const allTeamTasks = computed(() => {
    return teamMembers.value.flatMap((member) => member.tasks);
});

const filteredTeamMembers = computed(() => {
    let members = teamMembers.value;

    if (selectedTeamMember.value !== "all") {
        members = members.filter((m) => m.id === selectedTeamMember.value);
    }

    return members
        .map((member) => ({
            ...member,
            tasks: member.tasks.filter((task) => {
                let match = true;

                if (filterStatus.value !== "all") {
                    match = match && task.status === filterStatus.value;
                }

                if (filterPriority.value !== "all") {
                    if (filterPriority.value === "high") {
                        match = match && task.priorityLevel >= 8;
                    } else if (filterPriority.value === "medium") {
                        match =
                            match &&
                            task.priorityLevel >= 4 &&
                            task.priorityLevel < 8;
                    } else {
                        match = match && task.priorityLevel < 4;
                    }
                }

                return match;
            })
        }))
        .filter((member) => member.tasks.length > 0);
});

const fetchData = async () => {
    loading.value = true;
    error.value = null;

    try {
        if (!userId.value) {
            throw new Error("User ID not found. Please log in again.");
        }

        const response = await fetch(
            `http://127.0.0.1:4100/uid/${userId.value}`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        const data = await response.json();

        userData.value = {
            user_id: data.user_id,
            user_name: data.user_name,
            user_role: data.user_role,
            user_dept: data.user_dept
        };

        projects.value = data.projects.map((project) => ({
            id: project.id,
            name: project.name,
            desc: project.desc
        }));

        allTasks.value = data.projects.flatMap((project) =>
            project.tasks.map((task) => ({
                ...task,
                project: {
                    id: project.id,
                    name: project.name
                }
            }))
        );

        const memberMap = new Map();

        data.projects.forEach((project) => {
            project.members.forEach((memberId) => {
                if (memberId !== userId.value && !memberMap.has(memberId)) {
                    memberMap.set(memberId, {
                        id: memberId,
                        name: "Unknown",
                        tasks: []
                    });
                }
            });

            project.tasks.forEach((task) => {
                if (task.created_by && task.created_by.id !== userId.value) {
                    if (!memberMap.has(task.created_by.id)) {
                        memberMap.set(task.created_by.id, {
                            id: task.created_by.id,
                            name: task.created_by.name,
                            tasks: []
                        });
                    } else {
                        const member = memberMap.get(task.created_by.id);
                        if (member.name === "Unknown") {
                            member.name = task.created_by.name;
                        }
                    }

                    memberMap.get(task.created_by.id).tasks.push({
                        ...task,
                        project: { id: project.id, name: project.name }
                    });
                }

                if (task.collaborators) {
                    task.collaborators.forEach((collab) => {
                        if (collab.id !== userId.value) {
                            if (!memberMap.has(collab.id)) {
                                memberMap.set(collab.id, {
                                    id: collab.id,
                                    name: collab.name,
                                    tasks: []
                                });
                            } else {
                                const member = memberMap.get(collab.id);
                                if (member.name === "Unknown") {
                                    member.name = collab.name;
                                }
                            }

                            const member = memberMap.get(collab.id);
                            if (!member.tasks.some((t) => t.id === task.id)) {
                                member.tasks.push({
                                    ...task,
                                    project: {
                                        id: project.id,
                                        name: project.name
                                    }
                                });
                            }
                        }
                    });
                }
            });
        });

        teamMembers.value = Array.from(memberMap.values());
    } catch (err) {
        console.error("Error fetching data:", err);
        error.value = err.message || "An error occurred while fetching data";
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchData();
});
</script>
