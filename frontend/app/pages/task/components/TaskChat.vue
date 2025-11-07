<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { 
  Send, 
  Paperclip, 
  CheckCheck, 
  Edit2, 
  Trash2, 
  X,
  File,
  Image as ImageIcon,
  FileText,
  Download
} from 'lucide-vue-next'
import { useToast } from '@/components/ui/toast'

// Types
interface User {
  id: string
  email: string
  name: string
  role: string
}

interface MessageSender {
  name: string
  email: string | null
  avatar?: string | null
}

interface MessageAttachment {
  name: string
  url: string  // Will be base64 data URL
  type: string
  size: number
}

interface ChatMessage {
  id: string
  sender_id: string
  sender_name: string
  sender: MessageSender
  message: string
  mentions: string[]
  attachments: MessageAttachment[]
  timestamp: string
  edited: boolean
  edited_at: string | null
}

interface Collaborator {
  id: string
  name: string
}

interface MessagesResponse {
  task_id: string
  messages: ChatMessage[]
  count: number
}

// Props
const props = defineProps<{
  taskId: string
}>()

// User data from middleware
const userData = useState<{ user: User }>("userData")
const user = computed(() => userData.value?.user)

const { toast } = useToast()
const messageInput = ref('')
const messageInputRef = ref<InstanceType<typeof Input> | null>(null)
const messages = ref<ChatMessage[]>([])
const loading = ref(false)
const messagesContainerRef = ref<HTMLElement | null>(null)
const editingMessageId = ref<string | null>(null)
const editingText = ref('')

// Mention autocomplete
const showMentionDropdown = ref(false)
const mentionSearchTerm = ref('')
const mentionCursorPosition = ref(0)
const collaborators = ref<Collaborator[]>([])

// File attachments
const attachments = ref<MessageAttachment[]>([])
const fileInput = ref<HTMLInputElement | null>(null)
const uploadingFiles = ref(false)

// Format timestamp helper
const formatTimestamp = (timestamp: string) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-GB', { 
    hour: 'numeric', 
    minute: '2-digit', 
    hour12: true 
  })
}

// Get date separator text
const getDateSeparator = (timestamp: string) => {
  const msgDate = new Date(timestamp)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  
  // Reset time to compare dates only
  msgDate.setHours(0, 0, 0, 0)
  today.setHours(0, 0, 0, 0)
  yesterday.setHours(0, 0, 0, 0)
  
  const diffTime = today.getTime() - msgDate.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays <= 7) return `${diffDays} days ago`
  
  return msgDate.toLocaleDateString('en-GB', { 
    month: 'short', 
    day: 'numeric', 
    year: msgDate.getFullYear() !== today.getFullYear() ? 'numeric' : undefined 
  })
}

// Group messages by date
const groupedMessages = computed(() => {
  const groups: Record<string, ChatMessage[]> = {}
  
  messages.value.forEach(msg => {
    const separator = getDateSeparator(msg.timestamp)
    if (!groups[separator]) {
      groups[separator] = []
    }
    groups[separator].push(msg)
  })
  
  return groups
})

// Get user initials for avatar
const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Convert file to Base64
const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = error => reject(error)
  })
}

// Format file size
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// Fetch messages
const fetchMessages = async () => {
  loading.value = true
  try {
    const response = await $fetch<MessagesResponse>(`http://localhost:8000/manage-task/tasks/${props.taskId}/messages`, {
      credentials: 'include'
    })
    messages.value = response.messages || []
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Failed to fetch messages:', error)
    toast({
      title: 'Error',
      description: 'Failed to load chat messages',
      variant: 'destructive'
    })
  } finally {
    loading.value = false
  }
}

// Handle file selection
const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return
  
  // Limit file size to 2MB for demo purposes (base64 makes files larger)
  const MAX_FILE_SIZE = 2 * 1024 * 1024 // 2MB
  
  uploadingFiles.value = true
  
  try {
    for (const file of Array.from(input.files)) {
      if (file.size > MAX_FILE_SIZE) {
        toast({
          title: 'File too large',
          description: `${file.name} exceeds 2MB limit`,
          variant: 'destructive'
        })
        continue
      }
      
      // Convert to base64
      const base64 = await fileToBase64(file)
      
      const attachment: MessageAttachment = {
        name: file.name,
        url: base64, // Store base64 data URL
        type: file.type,
        size: file.size
      }
      
      attachments.value.push(attachment)
    }
    
    // Reset input
    input.value = ''
  } catch (error) {
    console.error('Failed to process files:', error)
    toast({
      title: 'Error',
      description: 'Failed to process files',
      variant: 'destructive'
    })
  } finally {
    uploadingFiles.value = false
  }
}

const removeAttachment = (index: number) => {
  attachments.value.splice(index, 1)
}

// Send message
const sendMessage = async () => {
  if (!messageInput.value.trim() && attachments.value.length === 0) return
  if (!user.value?.id) return
  
  try {
    // Extract mentions from message (@username)
    const mentionRegex = /@(\w+)/g
    const mentions: string[] = []
    let match
    
    while ((match = mentionRegex.exec(messageInput.value)) !== null) {
      const username = match[1]
      if (username) {
        const foundUser = collaborators.value.find(c => 
          c.name.toLowerCase().includes(username.toLowerCase())
        )
        if (foundUser) {
          mentions.push(foundUser.id)
        }
      }
    }
    
    // Construct the request body
    const requestBody = {
      message: messageInput.value,
      mentions: mentions,
      attachments: attachments.value, // Contains base64 URLs
      sender_id: user.value.id
    }
    
    console.log('[CHAT] Sending message with attachments:', {
      message: requestBody.message,
      attachmentCount: requestBody.attachments.length
    })
    
    await $fetch(`http://localhost:8000/manage-task/tasks/${props.taskId}/messages`, {
      method: 'POST',
      credentials: 'include',
      body: requestBody
    })
    
    messageInput.value = ''
    attachments.value = []
    await fetchMessages()
    
    toast({
      title: 'Success',
      description: 'Message sent'
    })
  } catch (error: any) {
    console.error('Failed to send message:', error)
    toast({
      title: 'Error',
      description: error.data?.detail || 'Failed to send message',
      variant: 'destructive'
    })
  }
}

// Edit message
const startEdit = (msg: ChatMessage) => {
  editingMessageId.value = msg.id
  editingText.value = msg.message
}

const cancelEdit = () => {
  editingMessageId.value = null
  editingText.value = ''
}

const saveEdit = async (messageId: string) => {
  if (!user.value?.id) return
  
  try {
    await $fetch(`http://localhost:8000/manage-task/tasks/${props.taskId}/messages/${messageId}`, {
      method: 'PUT',
      credentials: 'include',
      body: {
        message: editingText.value,
        user_id: user.value.id
      }
    })
    
    editingMessageId.value = null
    editingText.value = ''
    await fetchMessages()
    
    toast({
      title: 'Success',
      description: 'Message updated'
    })
  } catch (error) {
    console.error('Failed to edit message:', error)
    toast({
      title: 'Error',
      description: 'Failed to update message',
      variant: 'destructive'
    })
  }
}

// Delete message
const deleteMessage = async (messageId: string) => {
  if (!confirm('Delete this message?')) return
  if (!user.value?.id) return
  
  try {
    await $fetch(`http://localhost:8000/manage-task/tasks/${props.taskId}/messages/${messageId}`, {
      method: 'DELETE',
      credentials: 'include',
      body: {
        user_id: user.value.id
      }
    })
    
    await fetchMessages()
    
    toast({
      title: 'Success',
      description: 'Message deleted'
    })
  } catch (error) {
    console.error('Failed to delete message:', error)
    toast({
      title: 'Error',
      description: 'Failed to delete message',
      variant: 'destructive'
    })
  }
}

// Download attachment
const downloadAttachment = (attachment: MessageAttachment) => {
  const link = document.createElement('a')
  link.href = attachment.url // Base64 data URL
  link.download = attachment.name
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Get file icon based on type
const getFileIcon = (type: string) => {
  if (type.startsWith('image/')) return ImageIcon
  if (type.includes('pdf') || type.includes('document')) return FileText
  return File
}

// Scroll to bottom
const scrollToBottom = () => {
  nextTick(() => {
    setTimeout(() => {
      if (messagesContainerRef.value) {
        messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight + 1000
      }
    }, 100)
  })
}

// ✅ FIXED: Mention autocomplete logic - show dropdown immediately after @
const updateMentionDropdown = () => {
  const cursorPos = mentionCursorPosition.value
  const textBeforeCursor = messageInput.value.slice(0, cursorPos)
  const atIndex = textBeforeCursor.lastIndexOf('@')
  
  // Show dropdown if @ is found and no space after it
  if (atIndex !== -1) {
    const textAfterAt = textBeforeCursor.slice(atIndex + 1)
    // Check if there's no space after @
    if (!textAfterAt.includes(' ')) {
      showMentionDropdown.value = true
      mentionSearchTerm.value = textAfterAt
      return
    }
  }
  
  showMentionDropdown.value = false
  mentionSearchTerm.value = ''
}

watch(messageInput, () => {
  updateMentionDropdown()
})

// Filtered collaborators for mention dropdown
const filteredCollaborators = computed(() => {
  if (!mentionSearchTerm.value) {
    return collaborators.value
  }
  return collaborators.value.filter(c => 
    c.name.toLowerCase().includes(mentionSearchTerm.value.toLowerCase())
  )
})

// Fetch collaborators for mentions
const fetchCollaborators = async () => {
  try {
    const response = await $fetch<{ task: { collaborators: Collaborator[] } }>(`http://localhost:8000/manage-task/tasks/${props.taskId}`, {
      credentials: 'include'
    })
    collaborators.value = response.task.collaborators || []
  } catch (error) {
    console.error('Failed to fetch collaborators:', error)
  }
}

// Insert mention
const insertMention = (collaborator: Collaborator) => {
  const atIndex = messageInput.value.lastIndexOf('@')
  const newText = 
    messageInput.value.slice(0, atIndex) + 
    `@${collaborator.name} ` + 
    messageInput.value.slice(mentionCursorPosition.value)
  
  messageInput.value = newText
  
  // Update cursor position to after the inserted mention
  const newCursorPos = atIndex + collaborator.name.length + 2 // +2 for @ and space
  mentionCursorPosition.value = newCursorPos
  
  // Close dropdown
  showMentionDropdown.value = false
  mentionSearchTerm.value = ''
  
  // Focus back on input and set cursor position
  nextTick(() => {
    const inputEl = messageInputRef.value?.$el?.querySelector('input') || messageInputRef.value?.$el
    if (inputEl && typeof inputEl.focus === 'function') {
      inputEl.focus()
      if (typeof inputEl.setSelectionRange === 'function') {
        inputEl.setSelectionRange(newCursorPos, newCursorPos)
      }
    }
  })
}

// Handle input change to track cursor position
const handleInputChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  mentionCursorPosition.value = target.selectionStart || 0
  // Trigger mention dropdown update
  nextTick(() => {
    updateMentionDropdown()
  })
}

// Lifecycle
onMounted(() => {
  fetchMessages()
  fetchCollaborators()
  
  // Poll for new messages every 60 seconds
  setInterval(fetchMessages, 60000)
})
</script>

<template>
  <Card class="border-0 shadow-sm bg-white dark:bg-slate-900 flex flex-col h-[600px]">
    <CardHeader class="pb-4 flex-shrink-0">
      <CardTitle class="text-base font-semibold text-slate-900 dark:text-slate-100">
        Chat
      </CardTitle>
      <CardDescription class="text-sm text-slate-600 dark:text-slate-400">
        Discuss this task with your team
      </CardDescription>
    </CardHeader>

    <CardContent class="flex-1 flex flex-col overflow-hidden p-0 relative">
      <!-- Messages Area -->
      <div 
        ref="messagesContainerRef"
        class="flex-1 overflow-y-auto px-6 py-4"
      >
        <div v-if="loading" class="flex items-center justify-center h-32">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>

        <div v-else-if="messages.length === 0" class="flex items-center justify-center h-32">
          <p class="text-sm text-slate-500 dark:text-slate-400">No messages yet. Start the conversation!</p>
        </div>

        <div v-else class="space-y-6">
          <!-- Message groups by date -->
          <div v-for="(msgs, dateLabel) in groupedMessages" :key="dateLabel" class="space-y-3">
            <!-- Date separator -->
            <div class="flex items-center justify-center my-4">
              <div class="bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded-full">
                <span class="text-xs font-medium text-slate-600 dark:text-slate-400">
                  {{ dateLabel }}
                </span>
              </div>
            </div>

            <!-- Messages for this date -->
            <div
              v-for="msg in msgs"
              :key="msg.id"
              :class="`flex gap-3 ${msg.sender_id === user?.id ? 'flex-row-reverse' : ''}`"
            >
              <!-- Avatar (only for other users) -->
              <Avatar v-if="msg.sender_id !== user?.id" class="h-8 w-8 flex-shrink-0">
                <AvatarImage v-if="msg.sender.avatar" :src="msg.sender.avatar" :alt="msg.sender.name" />
                <AvatarFallback class="text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                  {{ getInitials(msg.sender.name) }}
                </AvatarFallback>
              </Avatar>

              <!-- Message bubble -->
              <div :class="`flex flex-col max-w-[75%] ${msg.sender_id === user?.id ? 'items-end' : 'items-start'}`">
                <!-- Sender name (only for other users) -->
                <p v-if="msg.sender_id !== user?.id" class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-1 px-3">
                  {{ msg.sender.name }}
                </p>

                <!-- Message content -->
                <div :class="`rounded-2xl px-4 py-2.5 ${
                  msg.sender_id === user?.id
                    ? 'bg-blue-600 text-white rounded-br-md'
                    : 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100 rounded-bl-md'
                }`">
                  <!-- Editing mode -->
                  <div v-if="editingMessageId === msg.id" class="space-y-2">
                    <Input
                      v-model="editingText"
                      class="text-sm"
                      @keyup.enter="saveEdit(msg.id)"
                      @keyup.esc="cancelEdit"
                    />
                    <div class="flex gap-2">
                      <Button size="sm" variant="ghost" @click="saveEdit(msg.id)" class="h-7 text-xs">
                        Save
                      </Button>
                      <Button size="sm" variant="ghost" @click="cancelEdit" class="h-7 text-xs">
                        Cancel
                      </Button>
                    </div>
                  </div>

                  <!-- Display mode -->
                  <div v-else>
                    <p v-if="msg.message" class="text-sm leading-relaxed whitespace-pre-wrap">{{ msg.message }}</p>

                    <!-- Attachments -->
                    <div v-if="msg.attachments && msg.attachments.length > 0" class="mt-3 space-y-2">
                      <div
                        v-for="(att, idx) in msg.attachments"
                        :key="idx"
                        :class="`rounded-lg overflow-hidden ${
                          msg.sender_id === user?.id
                            ? 'bg-blue-700'
                            : 'bg-white dark:bg-slate-700'
                        }`"
                      >
                        <!-- Image attachment -->
                        <div v-if="att.type.startsWith('image/')" class="relative group">
                          <img
                            :src="att.url"
                            :alt="att.name"
                            class="max-w-xs rounded cursor-pointer hover:opacity-90"
                            @click="downloadAttachment(att)"
                          />
                          <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <Button
                              size="sm"
                              variant="secondary"
                              class="h-8 w-8 p-0"
                              @click="downloadAttachment(att)"
                            >
                              <Download class="h-4 w-4" />
                            </Button>
                          </div>
                        </div>

                        <!-- Document attachment -->
                        <button
                          v-else
                          @click="downloadAttachment(att)"
                          :class="`flex items-center gap-2 p-3 w-full text-left hover:opacity-80 transition ${
                            msg.sender_id === user?.id
                              ? 'text-white'
                              : 'text-slate-900 dark:text-slate-100'
                          }`"
                        >
                          <component :is="getFileIcon(att.type)" class="w-5 h-5 flex-shrink-0" />
                          <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium truncate">{{ att.name }}</p>
                            <p class="text-xs opacity-75">{{ formatFileSize(att.size) }}</p>
                          </div>
                          <Download class="w-4 h-4 flex-shrink-0" />
                        </button>
                      </div>
                    </div>

                    <!-- Timestamp and actions -->
                    <div class="flex items-center gap-2 justify-between mt-1.5">
                      <span :class="`text-xs ${
                        msg.sender_id === user?.id 
                          ? 'text-blue-100' 
                          : 'text-slate-500 dark:text-slate-400'
                      }`">
                        {{ formatTimestamp(msg.timestamp) }}
                        <span v-if="msg.edited" class="ml-1">(edited)</span>
                      </span>

                      <!-- Action buttons (only for own messages) -->
                      <div v-if="msg.sender_id === user?.id" class="flex gap-1">
                        <Button
                          size="icon"
                          variant="ghost"
                          class="h-5 w-5 text-blue-100 hover:bg-blue-700"
                          @click="startEdit(msg)"
                        >
                          <Edit2 class="w-3 h-3" />
                        </Button>
                        <Button
                          size="icon"
                          variant="ghost"
                          class="h-5 w-5 text-blue-100 hover:bg-blue-700"
                          @click="deleteMessage(msg.id)"
                        >
                          <Trash2 class="w-3 h-3" />
                        </Button>
                      </div>

                      <!-- Read receipt (only for own messages) -->
                      <CheckCheck v-if="msg.sender_id === user?.id" class="w-3.5 h-3.5 text-blue-100" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ✅ FIXED: Mention dropdown - now contained within chatbox -->
      <div
        v-if="showMentionDropdown && filteredCollaborators.length > 0"
        class="absolute bottom-[calc(100%-24rem)] left-6 right-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-h-48 overflow-y-auto z-50"
      >
        <button
          v-for="collab in filteredCollaborators"
          :key="collab.id"
          @click="insertMention(collab)"
          class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-700 flex items-center gap-2 transition-colors"
        >
          <Avatar class="h-6 w-6">
            <AvatarFallback class="text-xs bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
              {{ getInitials(collab.name) }}
            </AvatarFallback>
          </Avatar>
          <span class="text-sm">{{ collab.name }}</span>
        </button>
      </div>

      <!-- Attachment preview -->
      <div v-if="attachments.length > 0" class="px-6 py-3 bg-slate-50 dark:bg-slate-800 border-t border-slate-100 dark:border-slate-700">
        <div class="flex flex-wrap gap-2">
          <div
            v-for="(att, idx) in attachments"
            :key="idx"
            class="relative group"
          >
            <!-- Image preview -->
            <div v-if="att.type.startsWith('image/')" class="relative w-16 h-16 rounded-lg overflow-hidden border-2 border-slate-200 dark:border-slate-600">
              <img :src="att.url" :alt="att.name" class="w-full h-full object-cover" />
              <button
                @click="removeAttachment(idx)"
                class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 opacity-0 group-hover:opacity-100 transition"
              >
                <X class="w-3 h-3" />
              </button>
            </div>

            <!-- Document preview -->
            <Badge v-else variant="secondary" class="flex items-center gap-1 pr-1">
              <component :is="getFileIcon(att.type)" class="w-3 h-3" />
              <span class="text-xs max-w-[100px] truncate">{{ att.name }}</span>
              <button @click="removeAttachment(idx)" class="hover:bg-slate-300 rounded p-0.5">
                <X class="w-3 h-3" />
              </button>
            </Badge>
          </div>
        </div>
        
        <!-- File size warning -->
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2">
          {{ attachments.length }} file(s) attached • Max 2MB per file
        </p>
      </div>

      <!-- Message Input -->
      <div class="flex items-center gap-2 px-6 py-4 border-t border-slate-100 dark:border-slate-800 flex-shrink-0 bg-white dark:bg-slate-900">
        <input
          ref="fileInput"
          type="file"
          multiple
          accept="image/*,.pdf,.doc,.docx,.txt"
          class="hidden"
          @change="handleFileSelect"
        />
        <Button
          variant="ghost"
          size="icon"
          class="h-10 w-10 text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:text-slate-400 dark:hover:bg-slate-800"
          @click="fileInput?.click()"
          :disabled="uploadingFiles"
        >
          <Paperclip class="w-5 h-5" :class="{ 'animate-pulse': uploadingFiles }" />
        </Button>
        <Input
          ref="messageInputRef"
          v-model="messageInput"
          type="text"
          placeholder="Type a message... (use @ to mention)"
          @keyup.enter="sendMessage"
          @input="handleInputChange"
          @keyup="handleInputChange"
          @click="handleInputChange"
          class="flex-1 text-sm border-slate-200 focus-visible:ring-blue-500 dark:border-slate-700 dark:bg-slate-800"
          :disabled="uploadingFiles"
        />
        <Button
          @click="sendMessage"
          size="icon"
          :disabled="(!messageInput.trim() && attachments.length === 0) || uploadingFiles"
          class="h-10 w-10 bg-blue-600 hover:bg-blue-700 text-white shadow-sm disabled:opacity-50"
        >
          <Send class="w-5 h-5" />
        </Button>
      </div>
    </CardContent>
  </Card>
</template>