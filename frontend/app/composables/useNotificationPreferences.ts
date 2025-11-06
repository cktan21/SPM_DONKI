/**
 * Composable for managing notification preferences
 * Stores preferences in localStorage and provides reactive state
 */
import { reactive, readonly } from "vue";

// All available notification event types from socket.ts
export const NOTIFICATION_EVENT_TYPES = [
    "task_created",
    "task_updated",
    "task_deleted",
    "task_assigned",
    "task_status_changed",
    "deadline_approaching",
    "deadline_overdue",
    "recurring_task_reset",
    "project_created",
    "project_collaborator_added",
] as const;

export type NotificationEventType = typeof NOTIFICATION_EVENT_TYPES[number];

const STORAGE_KEY = "notification_preferences";

type NotificationPreferences = Record<NotificationEventType, boolean>;

/**
 * Get default preferences (all enabled)
 */
function getDefaultPreferences(): NotificationPreferences {
    return Object.fromEntries(
        NOTIFICATION_EVENT_TYPES.map((type) => [type, true])
    ) as NotificationPreferences;
}

/**
 * Load preferences from localStorage
 */
function loadPreferences(): NotificationPreferences {
    if (typeof window === "undefined") {
        return getDefaultPreferences();
    }

    try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (!stored) {
            return getDefaultPreferences();
        }

        const parsed = JSON.parse(stored);
        
        // Ensure all event types are present with boolean values
        const preferences: NotificationPreferences = Object.fromEntries(
            NOTIFICATION_EVENT_TYPES.map((type) => [
                type,
                parsed[type] ?? true // Default to true if not found
            ])
        ) as NotificationPreferences;
        
        return preferences;
    } catch (error) {
        console.error("Error loading notification preferences:", error);
        return getDefaultPreferences();
    }
}

/**
 * Save preferences to localStorage
 */
function savePreferences(preferences: NotificationPreferences): void {
    if (typeof window === "undefined") return;

    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
    } catch (error) {
        console.error("Error saving notification preferences:", error);
    }
}

export const useNotificationPreferences = () => {
    // Load initial preferences
    const loaded = loadPreferences();
    
    // Save defaults if they don't exist in localStorage (first time initialization)
    if (typeof window !== "undefined") {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (!stored) {
            savePreferences(loaded);
        }
    }
    
    // Reactive state - use a reactive object instead of Map for better Vue reactivity
    const preferences = reactive<Record<NotificationEventType, boolean>>(
        { ...loaded } as Record<NotificationEventType, boolean>
    );

    /**
     * Save current preferences to localStorage
     */
    const saveCurrentPreferences = () => {
        savePreferences(preferences as NotificationPreferences);
    };

    /**
     * Check if a notification type is enabled
     */
    const isEnabled = (eventType: NotificationEventType): boolean => {
        return preferences[eventType] ?? true; // Default to true
    };

    /**
     * Toggle a notification type
     */
    const toggle = (eventType: NotificationEventType): void => {
        preferences[eventType] = !preferences[eventType];
        saveCurrentPreferences();
    };

    /**
     * Enable a notification type
     */
    const enable = (eventType: NotificationEventType): void => {
        preferences[eventType] = true;
        saveCurrentPreferences();
    };

    /**
     * Disable a notification type
     */
    const disable = (eventType: NotificationEventType): void => {
        preferences[eventType] = false;
        saveCurrentPreferences();
    };

    /**
     * Enable all notification types
     */
    const enableAll = (): void => {
        NOTIFICATION_EVENT_TYPES.forEach((type) => {
            preferences[type] = true;
        });
        saveCurrentPreferences();
    };

    /**
     * Disable all notification types
     */
    const disableAll = (): void => {
        NOTIFICATION_EVENT_TYPES.forEach((type) => {
            preferences[type] = false;
        });
        saveCurrentPreferences();
    };

    /**
     * Reset to default (all enabled)
     */
    const reset = (): void => {
        enableAll();
    };

    return {
        preferences: readonly(preferences),
        isEnabled,
        toggle,
        enable,
        disable,
        enableAll,
        disableAll,
        reset,
        eventTypes: NOTIFICATION_EVENT_TYPES,
    };
};

