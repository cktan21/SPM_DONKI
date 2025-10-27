#!/bin/bash
set -e

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."

# Wait for Kafka readiness loop (important for KRaft!)
for i in {1..30}; do
  kafka-topics.sh --bootstrap-server kafka:9092 --list >/dev/null 2>&1 && break || sleep 2
done

# Create topics from JSON configuration
echo "Creating Kafka topics..."

# # Task Events Topic
# kafka-topics --create \
#   --bootstrap-server kafka:29092 \
#   --topic task-events \
#   --partitions 3 \
#   --replication-factor 1 \
#   --config cleanup.policy=delete \
#   --config retention.ms=604800000

# # Project Events Topic  
# kafka-topics --create \
#   --bootstrap-server kafka:29092 \
#   --topic project-events \
#   --partitions 3 \
#   --replication-factor 1 \
#   --config cleanup.policy=delete \
#   --config retention.ms=604800000

# Schedule Events Topic
kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic schedule-events \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete \
  --config retention.ms=604800000

# Notification Events Topic
kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic notification-events \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete \
  --config retention.ms=1209600000

# # User Events Topic
# kafka-topics --create \
#   --bootstrap-server kafka:29092 \
#   --topic user-events \
#   --partitions 3 \
#   --replication-factor 1 \
#   --config cleanup.policy=delete \
#   --config retention.ms=604800000

echo "Done ✅"