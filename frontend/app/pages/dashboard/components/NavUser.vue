<script setup lang="ts">
import { ref } from "vue";
import {
    BadgeCheck,
    Bell,
    ChevronsUpDown,
    CreditCard,
    LogOut,
    Sparkles
} from "lucide-vue-next";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import {
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar
} from "@/components/ui/sidebar";
import NotificationPreferencesDialog from "./NotificationPreferencesDialog.vue";

const props = defineProps<{
    user: {
        name: string;
        email: string;
        role: string;
        avatar: string;
    };
}>();

const { isMobile } = useSidebar();

// Notification preferences dialog state
const showNotificationPreferences = ref(false);

const openNotificationPreferences = () => {
    showNotificationPreferences.value = true;
};

const handleLogout = async () => {
    try {
        const response = await fetch("http://localhost:8000/user/logout", {
            method: "POST",
            credentials: "include", // Important: sends cookies
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            useState("userData").value = null;

            // Redirect to login
            await navigateTo("/auth/login");
        } else {
            console.error("Logout failed");
        }
    } catch (error) {
        console.error("Logout error:", error);
    }
};
</script>

<template>
    <SidebarMenu>
        <SidebarMenuItem>
            <DropdownMenu>
                <DropdownMenuTrigger as-child>
                    <SidebarMenuButton
                        size="lg"
                        class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground">
                        <Avatar class="h-8 w-8 rounded-lg">
                            <AvatarImage :src="user.avatar" :alt="user.name" />
                            <AvatarFallback class="rounded-lg">
                                CN
                            </AvatarFallback>
                        </Avatar>
                        <div
                            class="grid flex-1 text-left text-sm leading-tight">
                            <span class="truncate font-semibold">{{
                                user.name
                            }}</span>
                            <span class="truncate font-semibold">{{
                                user.role
                            }}</span>
                            <span class="truncate text-xs">{{
                                user.email
                            }}</span>
                        </div>
                        <ChevronsUpDown class="ml-auto size-4" />
                    </SidebarMenuButton>
                </DropdownMenuTrigger>
                <DropdownMenuContent
                    class="w-[--reka-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                    :side="isMobile ? 'bottom' : 'right'"
                    align="end"
                    :side-offset="4">
                    <DropdownMenuLabel class="p-0 font-normal">
                        <div
                            class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                            <Avatar class="h-8 w-8 rounded-lg">
                                <AvatarImage
                                    :src="user.avatar"
                                    :alt="user.name" />
                                <AvatarFallback class="rounded-lg">
                                    CN
                                </AvatarFallback>
                            </Avatar>
                            <div
                                class="grid flex-1 text-left text-sm leading-tight">
                                <span class="truncate font-semibold">{{
                                    user.name
                                }}</span>
                                <span class="truncate font-semibold">{{
                                    user.role
                                }}</span>
                                <span class="truncate text-xs">{{
                                    user.email
                                }}</span>
                            </div>
                        </div>
                    </DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuGroup>
                    </DropdownMenuGroup>
                    <DropdownMenuSeparator />
                    <DropdownMenuGroup>
                        <DropdownMenuItem @click="openNotificationPreferences">
                            <Bell />
                            Notifications
                        </DropdownMenuItem>
                    </DropdownMenuGroup>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem @click="handleLogout">
                        <LogOut />
                        Log out
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </SidebarMenuItem>
    </SidebarMenu>

    <!-- Notification Preferences Dialog -->
    <NotificationPreferencesDialog v-model:open="showNotificationPreferences" />
</template>
