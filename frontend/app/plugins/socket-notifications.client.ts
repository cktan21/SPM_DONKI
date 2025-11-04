import { toast } from "vue-sonner";
import { socket, formatNotificationMessage } from "~/components/socket";

export default defineNuxtPlugin(() => {

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

    // Register user when plugin loads (you may need to get userId from auth)
    // This should be called after user authentication
    // You can get the user ID from your auth system here
    // For example: const userId = useAuth().user?.id;
    // if (userId) {
    //     socket.emit("register_user", userId);
    // }
});
