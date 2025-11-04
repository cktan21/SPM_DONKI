import { watch } from "vue";
import { toast } from "vue-sonner";
import { socket, formatNotificationMessage } from "~/components/socket";

export default defineNuxtPlugin(() => {
    const userData = useState<{ user: { id: string; email: string; role: string; name: string } } | null>("userData");
    let registeredUserId: string | null = null;

    // Function to register user with Socket.IO server
    const registerUser = (userId: string) => {
        if (socket.connected && userId && userId !== registeredUserId) {
            socket.emit("register_user", userId);
            registeredUserId = userId;
            console.log(`[Socket.IO] Registered user: ${userId}`);
        }
    };

    // Function to handle user registration when conditions are met
    const handleUserRegistration = () => {
        const userId = userData.value?.user?.id;
        if (userId && socket.connected) {
            registerUser(userId);
        }
    };

    // Listen for notification events from Socket.IO
    socket.on("notification", (payload: any) => {
        const notification = formatNotificationMessage(payload);

        // Show toast notification based on variant using vue-sonner
        if (notification.variant === "error") {
            toast.error(notification.title, {
                description: notification.description,
            });
        } else if (notification.variant === "warning") {
            toast.warning(notification.title, {
                description: notification.description,
            });
        } else if (notification.variant === "success") {
            toast.success(notification.title, {
                description: notification.description,
            });
        } else {
            toast.info(notification.title, {
                description: notification.description,
            });
        }
    });

    // Register user when socket connects
    socket.on("connect", () => {
        console.log("[Socket.IO] Client connected, attempting to register user...");
        handleUserRegistration();
    });

    // Handle socket reconnection
    socket.on("reconnect", () => {
        console.log("[Socket.IO] Client reconnected, re-registering user...");
        registeredUserId = null; // Reset to allow re-registration
        handleUserRegistration();
    });

    // Watch for userData changes (e.g., user logs in)
    watch(userData, (newUserData) => {
        if (newUserData?.user?.id) {
            console.log("[Socket.IO] User data available, registering...");
            handleUserRegistration();
        } else {
            // User logged out - clear registration
            registeredUserId = null;
            console.log("[Socket.IO] User logged out, cleared registration");
        }
    }, { immediate: true });

    // Try to register immediately if socket is already connected and user is available
    if (socket.connected) {
        handleUserRegistration();
    }
});
