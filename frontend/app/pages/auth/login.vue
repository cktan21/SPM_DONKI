<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const router = useRouter();

// Random cover image
const coverImage = ref("")

onMounted(() => {
  const randomIndex = Math.floor(Math.random() * 6) + 1
  coverImage.value = `/auth_images/background_image_${randomIndex}.jpg`
})

// Form state
const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

const BASE_URL = "http://localhost:8000/user";

// Frontend validation function
function validateForm(): boolean {
  // Trim values to handle whitespace-only inputs
  const trimmedEmail = email.value.trim();
  const trimmedPassword = password.value.trim();

  // Check if both fields are empty
  if (!trimmedEmail && !trimmedPassword) {
    errorMessage.value = "Please enter your email and password";
    return false;
  }

  // Check if email is empty
  if (!trimmedEmail) {
    errorMessage.value = "Please enter your email";
    return false;
  }

  // Check if password is empty
  if (!trimmedPassword) {
    errorMessage.value = "Please enter your password";
    return false;
  }

  // Basic email format validation (optional)
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(trimmedEmail)) {
    errorMessage.value = "Please enter a valid email address";
    return false;
  }

  // Clear any previous error messages if validation passes
  errorMessage.value = "";
  return true;
}

async function handleLogin() {
  // Run frontend validation first
  if (!validateForm()) {
    return; // Stop here if validation fails
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
  <div class="w-full h-screen lg:grid lg:grid-cols-2">
    <!-- Login Form -->
    <div class="flex items-center justify-center min-h-screen lg:py-12">
      <div class="mx-auto grid w-[350px] gap-6">
        <div class="grid gap-2 text-center">
          <h1 class="text-3xl font-bold">Login</h1>
          <p class="text-balance text-muted-foreground">
            Enter your email below to login
          </p>
        </div>

        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input 
              id="email" 
              type="email" 
              placeholder="hello@spmdonki.com" 
              v-model="email" 
              required 
              :class="{ 'border-red-500': errorMessage && !email.trim() }"
            />
          </div>

          <div class="grid gap-2">
            <Label for="password">Password</Label>
            <Input 
              id="password" 
              type="password" 
              v-model="password" 
              required 
              :class="{ 'border-red-500': errorMessage && !password.trim() }"
            />
          </div>

          <Button :disabled="loading" @click="handleLogin" class="w-full">
            {{ loading ? "Logging in..." : "Login" }}
          </Button>

          <p v-if="errorMessage" class="text-red-500 text-sm text-center">{{ errorMessage }}</p>
        </div>

        <div class="mt-4 text-center text-sm">
          Don't have an account? <a href="./signup" class="underline">Sign up</a>
        </div>
      </div>
    </div>

    <!-- Cover image -->
    <div class="hidden lg:block">
      <img v-if="coverImage" :src="coverImage" alt="Cover image" class="h-screen w-full object-cover dark:brightness-[0.2] dark:grayscale" />
    </div>
  </div>
</template>