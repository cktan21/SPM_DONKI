import { io, Socket } from "socket.io-client";

// Initialize Socket.IO client
// In Nuxt, the server runs on the same origin, so we can use relative URL
// The path should match the server route (/socket.io/)
export const socket: Socket = io({
    path: "/socket.io/",
    transports: ["websocket", "polling"],
    autoConnect: true,
});

// Notification event types
export interface NotificationPayload {
    event_type?: string;
    eventType?: string; // Support both formats
    data: {
        uid?: string;
        // user_id?: string;
        // userId?: string;
        task_name?: string;
        tid?: string;
        project_id?: string;
        project_name?: string;
        name?: string;
        email?: string;
        added_by_name?: string;
        created_by_uid?: string;
        priority_level?: number;
        old_status?: string;
        new_status?: string;
        label?: string;
        status?: string;
        description?: string;
        is_creator?: boolean;
        is_collaborator?: boolean;
        [key: string]: any;
    };
    timestamp: string;
}

// Helper function to format notification message based on event type
export function formatNotificationMessage(payload: NotificationPayload): {
    title: string;
    description: string;
    variant?: "default" | "success" | "warning" | "error" | "info";
} {
    // Support both event_type (snake_case) and eventType (camelCase)
    const eventType = payload.event_type || payload.eventType || "unknown";
    const { data } = payload;

    const taskName = data.task_name || "Task";
    const userName = data.name || "User";
    const projectName = data.project_name || "Project";
    const addedByName = data.added_by_name || "Someone";

    const oldStatusText = data.old_status ? ` from ${data.old_status}` : "";
    const newStatusText = data.new_status ? ` to ${data.new_status}` : "";

    switch (eventType) {
        case "task_created":
            return {
                title: "New Task Created",
                description: `${taskName} has been created${data.project_name ? ` in ${data.project_name}` : ""}`,
                variant: "info",
            };
        case "task_updated":
            return {
                title: "Task Updated",
                description: `${taskName} has been updated`,
                variant: "info",
            };
        case "task_deleted":
            return {
                title: "Task Deleted",
                description: `${taskName} has been deleted`,
                variant: "warning",
            };
        case "task_assigned":
            const priorityText = data.priority_level ? ` (Priority: ${data.priority_level})` : "";
            const labelText = data.label ? ` [${data.label}]` : "";

            // Different messages based on whether user is the creator
            if (data.is_creator === true) {
                return {
                    title: "Task Created & Assigned",
                    description: `You've created and been assigned to "${taskName}"${priorityText}${labelText}`,
                    variant: "success",
                };
            } else {
                const assignedBy = userName && userName !== "User" ? ` by ${userName}` : "";
                return {
                    title: "Task Assigned",
                    description: `You've been assigned to "${taskName}"${assignedBy}${priorityText}${labelText}`,
                    variant: "success",
                };
            }
        case "task_status_changed":
            const statusText = data.status ? ` to ${data.status}` : "";
            return {
                title: "Task Status Changed",
                description: `Status of ${taskName} has been changed${oldStatusText}${newStatusText}`,
                variant: "info",
            };
        case "deadline_approaching":
            return {
                title: "Deadline Approaching",
                description: `${taskName} deadline is approaching (3 days remaining)`,
                variant: "warning",
            };
        case "deadline_overdue":
            return {
                title: "Deadline Overdue",
                description: `${taskName} deadline has passed`,
                variant: "warning",
            };
        case "project_created":
            return {
                title: "New Project Created",
                description: `A new project${projectName !== "Project" ? ` "${projectName}"` : ""} has been created`,
                variant: "info",
            };
        case "project_collaborator_added":
            const taskContext = taskName && taskName !== "Task" ? ` for task "${taskName}"` : "";
            return {
                title: "Added to Project",
                description: `${addedByName} added you to project "${projectName}"${taskContext}`,
                variant: "success",
            };
        default:
            return {
                title: "Notification",
                description: `Event: ${eventType}`,
                variant: "default",
            };
    }
}

