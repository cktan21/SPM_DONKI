import { watch } from "vue";
import { toast } from "@/components/ui/toast";
import { socket, formatNotificationMessage } from "~/components/socket";

export default defineNuxtPlugin(() => {
    console.log("[Socket.IO Plugin] Initializing...");
    console.log("[Socket.IO Plugin] Socket connected:", socket.connected);
    console.log("[Socket.IO Plugin] Socket ID:", socket.id);
    console.log("[Socket.IO Plugin] Toast function available:", typeof toast);

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
        console.log("[Socket.IO Client] Received notification:", payload);

        try {
            const notification = formatNotificationMessage(payload);
            console.log("[Socket.IO Client] Formatted notification:", notification);

            // Show toast notification using shadcn toast
            // Map notification variants to shadcn toast variants
            // shadcn toast only supports "default" and "destructive" variants
            const toastVariant = notification.variant === "error" ? "destructive" : "default";

            toast({
                title: notification.title,
                description: notification.description,
                variant: toastVariant,
            });

            console.log("[Socket.IO Client] Toast notification displayed");
        } catch (error) {
            console.error("[Socket.IO Client] Error processing notification:", error);
        }
    });

    // Register user when socket connects
    socket.on("connect", () => {
        console.log("[Socket.IO Plugin] Client connected, socket ID:", socket.id);
        console.log("[Socket.IO Plugin] Attempting to register user...");
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
