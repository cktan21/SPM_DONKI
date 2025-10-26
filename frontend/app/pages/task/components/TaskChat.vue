<script setup lang="ts">
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Send, Paperclip, CheckCheck } from 'lucide-vue-next'

const messageInput = ref('')

const mockMessages = ref([
  { id: '1', sender: 'Alex Chen', message: 'Started working on the wireframes', timestamp: '10:30 AM', isOwn: false },
  { id: '2', sender: 'You', message: 'Great! Let me know if you need any feedback', timestamp: '10:32 AM', isOwn: true },
  { id: '3', sender: 'Maria Garcia', message: 'I can help with the chart components once wireframes are done', timestamp: '11:15 AM', isOwn: false },
  { id: '4', sender: 'You', message: 'Perfect timing! We should be ready by next week', timestamp: '11:20 AM', isOwn: true },
])

const sendMessage = () => {
  if (!messageInput.value.trim()) return
  const now = new Date()
  const timestamp = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
  
  mockMessages.value.push({
    id: Date.now().toString(),
    sender: 'You',
    message: messageInput.value,
    timestamp,
    isOwn: true
  })
  messageInput.value = ''
}
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900">
    <CardHeader class="pb-4">
      <CardTitle class="text-base font-semibold text-slate-900 dark:text-slate-100">Chat</CardTitle>
      <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
        Discuss this task with your team
      </CardDescription>
    </CardHeader>
    <CardContent class="space-y-4">
      <!-- Messages -->
      <div class="space-y-3 max-h-96 overflow-y-auto">
        <div
          v-for="msg in mockMessages"
          :key="msg.id"
          :class="`flex ${msg.isOwn ? 'justify-end' : 'justify-start'}`"
        >
          <div :class="`max-w-[75%] ${msg.isOwn ? 'items-end' : 'items-start'} flex flex-col`">
            <p v-if="!msg.isOwn" class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-1 px-3">
              {{ msg.sender }}
            </p>
            <div :class="`rounded-2xl px-4 py-2.5 ${
              msg.isOwn 
                ? 'bg-blue-600 text-white rounded-br-md' 
                : 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 rounded-bl-md'
            }`">
              <p class="text-sm leading-relaxed">{{ msg.message }}</p>
              <div class="flex items-center gap-1.5 justify-end mt-1.5">
                <span :class="`text-xs ${msg.isOwn ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'}`">
                  {{ msg.timestamp }}
                </span>
                <CheckCheck v-if="msg.isOwn" class="w-3.5 h-3.5 text-blue-100" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="flex items-center gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
        <Button variant="ghost" size="icon" class="h-10 w-10 text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:text-slate-400 dark:hover:bg-slate-800">
          <Paperclip class="w-5 h-5" />
        </Button>
        <Input
          v-model="messageInput"
          type="text"
          placeholder="Type a message..."
          @keyup.enter="sendMessage"
          class="flex-1 text-sm border-slate-200 focus-visible:ring-blue-500 dark:border-slate-700 dark:bg-slate-800"
        />
        <Button @click="sendMessage" size="icon" class="h-10 w-10 bg-blue-600 hover:bg-blue-700 text-white shadow-sm">
          <Send class="w-5 h-5" />
        </Button>
      </div>
    </CardContent>
  </Card>
</template>