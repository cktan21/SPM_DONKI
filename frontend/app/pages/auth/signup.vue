<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const router = useRouter()

// Random cover image
const randomIndex = Math.floor(Math.random() * 6) + 1
const coverImage = `/auth_images/background_image_${randomIndex}.jpg`

// Form state
const email = ref("")
const password = ref("")
const loading = ref(false)
const errorMessage = ref("")

const BASE_URL = "http://localhost:8000/user"

// ----------------------
// Auto-redirect if already authenticated
// ----------------------
const checkedAuth = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`${BASE_URL}/me`, {
      method: "GET",
      credentials: "include" // send cookies automatically
    })
    if (res.ok) {
      router.replace("/dashboard") // already logged in
    }
  } catch {
    // not logged in, show signup form
  } finally {
    checkedAuth.value = true
  }
})

// ----------------------
// Signup handler
// ----------------------
async function handleSignup() {
  loading.value = true
  errorMessage.value = ""

  try {
    const res = await fetch(`${BASE_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // cookies will be set by backend
      body: JSON.stringify({ email: email.value, password: password.value })
    })

    const data = await res.json().catch(() => ({}))

    if (!res.ok) {
      errorMessage.value = data.detail || `Signup failed (${res.status})`
      return
    }

    // Success → cookies already set by backend
    router.replace("/dashboard")

  } catch (err: any) {
    errorMessage.value = err.message || "Network error"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-if="checkedAuth" class="w-full h-screen lg:grid lg:grid-cols-2">
    <!-- Left side: Signup form -->
    <div class="flex items-center justify-center min-h-screen lg:py-12">
      <div class="mx-auto grid w-[350px] gap-6">
        <div class="grid gap-2 text-center">
          <h1 class="text-3xl font-bold">Sign Up</h1>
          <p class="text-balance text-muted-foreground">
            Create a new account by entering your email and password
          </p>
        </div>

        <!-- Form -->
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input id="email" type="email" placeholder="hello@example.com" v-model="email" required />
          </div>

          <div class="grid gap-2">
            <Label for="password">Password</Label>
            <Input id="password" type="password" v-model="password" required />
          </div>

          <Button :disabled="loading" @click="handleSignup" class="w-full">
            {{ loading ? "Signing up..." : "Sign Up" }}
          </Button>

          <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
        </div>

        <!-- Login link -->
        <div class="mt-4 text-center text-sm">
          Already have an account? <a href="./login" class="underline">Login</a>
        </div>
      </div>
    </div>

    <!-- Right side: Cover image -->
    <div class="hidden lg:block">
      <img :src="coverImage" alt="Cover image" class="h-screen w-full object-cover dark:brightness-[0.2] dark:grayscale" />
    </div>
  </div>
</template>
