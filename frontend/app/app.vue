<template>
  <div>
    <Toaster position="top-right" closeButton closeButtonPosition="top-right" theme="system"/>
    <NuxtPage />
  </div>
</template>

<script lang="ts" setup>
const { $toast } = useNuxtApp()
</script>