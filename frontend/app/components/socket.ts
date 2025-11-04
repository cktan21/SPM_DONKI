import { io, Socket } from "socket.io-client";

export const socket: Socket = io();

// Notification event types
export interface NotificationPayload {
    eventType: string;
    data: {
        uid?: string;
        user_id?: string;
        userId?: string;
        task_name?: string;
        tid?: string;
        project_id?: string;
        name?: string;
        email?: string;
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
    const { eventType, data } = payload;
    const taskName = data.task_name || "Task";
    const userName = data.name || "User";

    switch (eventType) {
        case "task_created":
            return {
                title: "New Task Created",
                description: `${taskName} has been created`,
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
            return {
                title: "Task Assigned",
                description: `You have been assigned to ${taskName}`,
                variant: "success",
            };
        case "task_status_changed":
            return {
                title: "Task Status Changed",
                description: `Status of ${taskName} has been changed`,
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
                variant: "error",
            };
        case "project_created":
            return {
                title: "New Project Created",
                description: `A new project has been created`,
                variant: "info",
            };
        case "project_collaborator_added":
            return {
                title: "Added to Project",
                description: `You have been added to a project`,
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

