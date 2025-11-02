<script setup lang="ts">
import type { SidebarProps } from "@/components/ui/sidebar"

import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  CheckSquare,
  GalleryVerticalEnd,
  Map,
  PieChart,
  ClipboardList,
  ChartNoAxesColumnIncreasing,
  Settings2,
  SquareTerminal,
} from "lucide-vue-next"
import NavMain from "./NavMain.vue"
import NavProjects from "./NavProjects.vue"
import NavUser from "./NavUser.vue"
import TeamSwitcher from "./TeamSwitcher.vue"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: "icon",
})

// ✅ Grab the user info (comes from middleware auth.global.ts)
const userData = useState<any>("userData")
const role = userData.value?.user?.role
const email = userData.value?.user?.email
const name = userData.value?.user?.name
// This is sample data.
const data = {
  user: {
    role: role,
    email: email,
    name: name,
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Don Donki",
      logo: GalleryVerticalEnd,
      plan: "Enterprise",
    },
    // {
    //   name: "Acme Corp.",
    //   logo: AudioWaveform,
    //   plan: "Startup",
    // },
    // {
    //   name: "Evil Corp.",
    //   logo: Command,
    //   plan: "Free",
    // },
  ],
  navMain: [
    {
      title: "Report",
      url: "#",
      icon: BookOpen,
      items: [
        // {
        //   title: "Introduction",
        //   url: "#",
        // },
        // {
        //   title: "Get Started",
        //   url: "#",
        // },
 // ✅ Show this only if role === "hr"
        ...(["hr","manager", "admin"].includes(userData.value?.user?.role)
          ? [{ title: "Generate Report", url: "/generatereport" }]
          : []),
        // {
        //   title: "Changelog",
        //   url: "#",
        // },
      ],
    },
  ],
  projects: [
    ...(["staff","manager"].includes(userData.value?.user?.role)
      ? [{ name: "Task", url: "/task", icon: CheckSquare}, { name: "Timeline", url: "/timeline", icon: ChartNoAxesColumnIncreasing }]
      : []),
    ...(["manager"].includes(userData.value?.user?.role)
      ? [{ name: "Assign Task", url: "/assignTask", icon: ClipboardList }]
      : []),
    ...(["hr"].includes(userData.value?.user?.role)
      ? [{ name: "Create Signup", url: "/auth/signup", icon: ClipboardList }]
      : []),
  ],
}
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <TeamSwitcher :teams="data.teams" />
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
      <NavProjects :projects="data.projects" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="data.user" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
