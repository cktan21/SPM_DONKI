<script setup lang="ts">
definePageMeta({
  layout: false
})

// Use navigateTo server-side safe
if (process.client) {
  await navigateTo("/auth/login", { replace: true, external: false })
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-background">
    <p class="text-muted-foreground">Redirecting...</p>
  </div>
</template>