<script lang="ts">
export const description =
  "A login form with email and password. There's an option to login with Google and a link to sign up if you don't have an account."
export const iframeHeight = "600px"
</script>

<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

// Function to handle login click
const handleLogin = () => {
  alert("Hello")
}
</script>

<template>
  <!-- Full-screen flex container -->
  <div class="w-full h-screen flex items-center justify-center px-4">
    <Card class="mx-auto max-w-sm w-full">
      <CardHeader>
        <CardTitle class="text-2xl">Login</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="john.doe@spmdonki.com"
              required
            />
          </div>
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
              <a href="#" class="ml-auto inline-block text-sm underline">
                Forgot your password?
              </a>
            </div>
            <Input id="password" type="password" required />
          </div>
          <!-- Add @click event here -->
          <Button type="button" class="w-full" @click="handleLogin">Login</Button>
        </div>
        <div class="mt-4 text-center text-sm">
          Don't have an account?
          <a href="#" class="underline">Sign up</a>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
