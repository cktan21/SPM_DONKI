<script lang="ts" setup>
import { Toaster } from "@/components/ui/toast";
</script>

<template>
    <div>        
        <NuxtPage />
    </div>
    <ClientOnly>
        <Toaster />
    </ClientOnly>
</template>