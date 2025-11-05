import type { NitroApp } from "nitropack";
import { Server as Engine } from "engine.io";
import { Server } from "socket.io";
import { defineEventHandler } from "h3";
import { Kafka } from "kafkajs";

export default defineNitroPlugin(async (nitroApp: NitroApp) => {
    const engine = new Engine();
    const io = new Server();

    io.bind(engine);

    // Store connected socket IDs mapped to user IDs for filtering notifications
    const userSockets = new Map<string, Set<string>>();

    io.on("connection", (socket) => {
        console.log(`[Socket.IO] Client connected: ${socket.id}`);

        // Register user when they connect with their user ID
        socket.on("register_user", (userId: string) => {
            if (!userSockets.has(userId)) {
                userSockets.set(userId, new Set());
            }
            userSockets.get(userId)!.add(socket.id);
            console.log(`[Socket.IO] User ${userId} registered with socket ${socket.id}`);
        });

        socket.on("disconnect", (reason) => {
            console.log(`[Socket.IO] Client disconnected: ${socket.id}, reason: ${reason}`);
            // Clean up user socket mappings
            for (const [userId, sockets] of userSockets.entries()) {
                sockets.delete(socket.id);
                if (sockets.size === 0) {
                    userSockets.delete(userId);
                }
            }
        });
    });

    // Initialize Kafka consumer
    // Use localhost:9092 for frontend (host machine), or kafka:9093 if running inside Docker
    const kafkaBootstrapServers = process.env.KAFKA_BOOTSTRAP_SERVERS || "localhost:9092";

    const kafka = new Kafka({
        clientId: "nuxt-socketio-notification-consumer",
        brokers: [kafkaBootstrapServers],
        retry: {
            initialRetryTime: 100,
            retries: 8,
        },
        connectionTimeout: 10000, // 10 seconds
        requestTimeout: 30000, // 30 seconds
    });

    const consumer = kafka.consumer({
        groupId: "nuxt-frontend-notification-group",
        sessionTimeout: 30000,
        heartbeatInterval: 3000,
    });

    // Try to connect to Kafka, but don't fail if it's not available
    const connectToKafka = async () => {
        try {
            console.log(`[Kafka] Attempting to connect to ${kafkaBootstrapServers}...`);
            await consumer.connect();
            console.log("[Kafka] Consumer connected successfully");

            await consumer.subscribe({
                topic: "notification-events",
                fromBeginning: false,
            });
            console.log("[Kafka] Subscribed to topic: notification-events");

            // Start consuming messages
            await consumer.run({
                eachMessage: async ({ topic, partition, message }) => {
                    try {
                        // Deserialize the message
                        const messageValue = message.value?.toString();
                        if (!messageValue) {
                            console.warn("[Kafka] Received empty message");
                            return;
                        }

                        const parsedMessage = JSON.parse(messageValue);

                        // Extract event_type and data from the message
                        // Based on the backend structure, messages are published as:
                        // { event_type: "...", data: { ... } }
                        const eventType = parsedMessage.event_type || parsedMessage.eventType;
                        const eventData = parsedMessage.data || parsedMessage;

                        console.log(`[Kafka] Received notification event: ${eventType}`, eventData);

                        // Extract user ID from the event data to send notification to specific user
                        const targetUserId = eventData.uid || eventData.user_id || eventData.userId;

                        if (targetUserId) {
                            // Send notification to specific user's sockets
                            const userSocketIds = userSockets.get(targetUserId);
                            if (userSocketIds && userSocketIds.size > 0) {
                                const notificationPayload = {
                                    eventType,
                                    data: eventData,
                                    timestamp: new Date().toISOString(),
                                };

                                // Emit to all sockets for this user
                                for (const socketId of userSocketIds) {
                                    io.to(socketId).emit("notification", notificationPayload);
                                }

                                console.log(
                                    `[Socket.IO] Sent notification to user ${targetUserId} (${userSocketIds.size} socket(s))`
                                );
                            } else {
                                console.log(
                                    `[Socket.IO] No connected sockets for user ${targetUserId}, skipping notification`
                                );
                            }
                        } else {
                            // Broadcast to all connected clients if no specific user ID
                            io.emit("notification", {
                                eventType,
                                data: eventData,
                                timestamp: new Date().toISOString(),
                            });
                            console.log("[Socket.IO] Broadcasted notification to all clients");
                        }
                    } catch (error) {
                        console.error("[Kafka] Error processing message:", error);
                    }
                },
            });
        } catch (error: any) {
            console.warn(
                `[Kafka] Failed to connect to Kafka at ${kafkaBootstrapServers}. ` +
                `Socket.IO will continue to work, but notifications from Kafka won't be received. ` +
                `Error: ${error.message || error}`
            );
            console.warn(
                `[Kafka] Make sure Kafka is running and accessible. ` +
                `If running on host machine, use localhost:9092. ` +
                `If running inside Docker, use kafka:9092.`
            );
            // Continue execution even if Kafka fails - Socket.IO will still work
        }
    };

    // Connect to Kafka (non-blocking)
    connectToKafka().catch((error) => {
        console.error("[Kafka] Unexpected error during connection:", error);
    });

    // Cleanup on Nitro close
    nitroApp.hooks.hook("close", async () => {
        try {
            // Only disconnect if consumer was connected
            if (consumer) {
                await consumer.disconnect();
                console.log("[Kafka] Consumer disconnected");
            }
        } catch (error) {
            // Ignore errors during cleanup
            console.warn("[Kafka] Error during consumer cleanup (ignored):", error);
        }
    });

    nitroApp.router.use("/socket.io/", defineEventHandler({
        handler(event) {
            // @ts-expect-error engine.io types don't perfectly match Nitro's request/response
            engine.handleRequest(event.node.req, event.node.res);
            event._handled = true;
        },
        websocket: {
            open(peer) {
                // @ts-expect-error private method and property
                engine.prepare(peer._internal.nodeReq);
                // @ts-expect-error private method and property
                engine.onWebSocket(peer._internal.nodeReq, peer._internal.nodeReq.socket, peer.websocket);
            }
        }
    }));
});

