import { socket, formatNotificationMessage } from "~/components/socket";

export const useSocketNotifications = () => {
    return {
        socket,
        formatNotificationMessage,
    };
};
