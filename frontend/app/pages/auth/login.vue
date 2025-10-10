<script setup lang="ts">
definePageMeta({
  layout: false,
  colorMode: 'light' // Force light mode for this page
})

import { ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const router = useRouter();

// Random cover image
const coverImage = ref("")
const isReady = ref(false)

onMounted(async () => {
  const randomIndex = Math.floor(Math.random() * 6) + 1
  coverImage.value = `/auth_images/background_image_${randomIndex}.jpg`
  
  await nextTick()
  isReady.value = true
})

// Form state
const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

const BASE_URL = "http://localhost:8000/user";

function validateForm(): boolean {
  const trimmedEmail = email.value.trim();
  const trimmedPassword = password.value.trim();

  if (!trimmedEmail && !trimmedPassword) {
    errorMessage.value = "Please enter your email and password";
    return false;
  }

  if (!trimmedEmail) {
    errorMessage.value = "Please enter your email";
    return false;
  }

  if (!trimmedPassword) {
    errorMessage.value = "Please enter your password";
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(trimmedEmail)) {
    errorMessage.value = "Please enter a valid email address";
    return false;
  }

  errorMessage.value = "";
  return true;
}

async function handleLogin() {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  try {
    const res = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ 
        email: email.value.trim(), 
        password: password.value.trim() 
      })
    });

    if (!res.ok) {
      const data = await res.json();
      errorMessage.value = data.detail || `Login failed (${res.status})`;
      return;
    }

    console.log("Login successful — redirecting...");
    router.replace("/dashboard");

  } catch (err: any) {
    errorMessage.value = err.message || "Network error";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <!-- Force light mode wrapper -->
  <div class="light">
    <div v-if="isReady" class="w-full h-screen overflow-hidden bg-white">
      <div class="h-full lg:grid lg:grid-cols-2">
        <!-- Login Form -->
        <div class="flex items-center justify-center h-full py-12 px-4 bg-white">
          <div class="w-full max-w-[350px] grid gap-6">
            <div class="grid gap-2 text-center">
              <h1 class="text-3xl font-bold text-black">Login</h1>
              <p class="text-balance text-gray-600">
                Enter your email below to login
              </p>
            </div>

            <div class="grid gap-4">
              <div class="grid gap-2">
                <Label for="email" class="text-black">Email</Label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="hello@spmdonki.com" 
                  v-model="email" 
                  required 
                  :class="{ 'border-red-500': errorMessage && !email.trim() }"
                  class="bg-white text-black"
                />
              </div>

              <div class="grid gap-2">
                <Label for="password" class="text-black">Password</Label>
                <Input 
                  id="password" 
                  type="password" 
                  v-model="password" 
                  required 
                  :class="{ 'border-red-500': errorMessage && !password.trim() }"
                  class="bg-white text-black"
                />
              </div>

              <Button :disabled="loading" @click="handleLogin" class="w-full">
                {{ loading ? "Logging in..." : "Login" }}
              </Button>

              <p v-if="errorMessage" class="text-red-500 text-sm text-center">{{ errorMessage }}</p>
            </div>

            <div class="mt-4 text-center text-sm text-gray-600">
              Don't have an account? <a href="./signup" class="underline text-black">Sign up</a>
            </div>
          </div>
        </div>

        <!-- Cover image -->
        <div class="hidden lg:block h-full overflow-hidden">
          <img 
            v-if="coverImage" 
            :src="coverImage" 
            alt="Cover image" 
            class="h-full w-full object-cover" 
          />
        </div>
      </div>
    </div>
    <div v-else class="w-full h-screen flex items-center justify-center bg-white">
      <p class="text-gray-600">Loading...</p>
    </div>
  </div>
</template>