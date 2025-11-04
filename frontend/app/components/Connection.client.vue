<script setup lang="ts">
import { socket } from "./socket";

const isConnected = ref(false);
const transport = ref("N/A");
const messages = ref<Array<{ id: string; data: any; timestamp: string }>>([]);

function onConnect() {
    isConnected.value = true;
    transport.value = socket.io.engine.transport.name;

    socket.io.engine.on("upgrade", (rawTransport) => {
        transport.value = rawTransport.name;
    });
}

function onDisconnect() {
    isConnected.value = false;
    transport.value = "N/A";
}

function sendMessage() {
    if (socket.connected) {
        socket.emit("message", {
            text: `Hello from client at ${new Date().toLocaleTimeString()}`
        });
    }
}

// Set up socket listeners
onMounted(() => {
    // Check if already connected
    if (socket.connected) {
        onConnect();
    }

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);
    socket.on("message", (data) => {
        messages.value.push(data);
    });
});

onBeforeUnmount(() => {
    socket.off("connect", onConnect);
    socket.off("disconnect", onDisconnect);
    socket.off("message");
});
</script>

<template>
    <div class="p-4 border rounded-lg space-y-4">
        <div class="space-y-2">
            <div class="flex items-center gap-2">
                <div
                    :class="[
                        'h-3 w-3 rounded-full',
                        isConnected ? 'bg-green-500' : 'bg-red-500'
                    ]" />
                <p class="font-semibold">
                    Status: {{ isConnected ? "connected" : "disconnected" }}
                </p>
            </div>
            <p class="text-sm text-gray-600">Transport: {{ transport }}</p>
        </div>

        <div class="space-y-2">
            <button
                @click="sendMessage"
                :disabled="!isConnected"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed">
                Send Test Message
            </button>
        </div>

        <div v-if="messages.length > 0" class="space-y-2">
            <h3 class="font-semibold">Messages:</h3>
            <div class="space-y-1 max-h-48 overflow-y-auto">
                <div
                    v-for="(msg, index) in messages"
                    :key="index"
                    class="p-2 bg-gray-100 rounded text-sm">
                    <div class="font-mono text-xs text-gray-500">
                        {{ msg.timestamp }}
                    </div>
                    <div>{{ JSON.stringify(msg.data, null, 2) }}</div>
                </div>
            </div>
        </div>
    </div>
</template>
