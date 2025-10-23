# Kafka Setup for SPM Project

This directory contains Kafka configuration and setup files for the SPM (Software Project Management) microservices architecture.

## Overview

Kafka is used for event-driven communication between microservices, enabling:

-   Asynchronous event processing
-   Event sourcing and audit trails
-   Decoupled service communication
-   Real-time notifications
-   Event replay capabilities

## Architecture

### Topics

1. **task-events**: Task-related events (created, updated, deleted, assigned)
2. **project-events**: Project-related events (created, updated, deleted, collaborator changes)
3. **schedule-events**: Schedule and deadline events (created, updated, overdue, approaching)
4. **user-events**: User-related events (created, updated, deleted)
5. **notification-events**: Notification delivery events (sent, delivered, failed)

### Event Types

#### Task Events

-   `task_created`: New task created
-   `task_updated`: Task details updated
-   `task_deleted`: Task removed
-   `task_assigned`: Task assigned to user
-   `task_status_changed`: Task status updated

#### Project Events

-   `project_created`: New project created
-   `project_updated`: Project details updated
-   `project_deleted`: Project removed
-   `project_collaborator_added`: User added to project
-   `project_collaborator_removed`: User removed from project

#### Schedule Events

-   `schedule_created`: New schedule created
-   `schedule_updated`: Schedule details updated
-   `schedule_deleted`: Schedule removed
-   `deadline_approaching`: Deadline within 3 days
-   `deadline_overdue`: Deadline has passed

## Setup Instructions

### 1. Start Kafka Services

```bash
# Start all services including Kafka
docker-compose up -d

# Or start only Kafka services
docker-compose up -d zookeeper kafka kafka-ui kafka-setup
```

### 2. Verify Kafka is Running

```bash
# Check if topics are created
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check Kafka UI (optional)
# Open http://localhost:8080 in your browser
```

### 3. Environment Variables

Add these to your `.env` file:

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=spm-consumer-group
```

## Usage in Services

### Publishing Events

```python
from kafka_events import TaskEventPublisher

# Initialize publisher
task_publisher = TaskEventPublisher()

# Publish task created event
task_publisher.publish_task_created({
    'id': 'task-123',
    'name': 'New Task',
    'created_by_uid': 'user-456',
    'pid': 'project-789'
})

# Close connection
task_publisher.close()
```

### Consuming Events

```python
from kafka_client import KafkaEventConsumer, Topics

def handle_task_event(event):
    print(f"Received event: {event['event_type']}")
    print(f"Data: {event['data']}")

# Initialize consumer
consumer = KafkaEventConsumer()
consumer.subscribe_to_topics([Topics.TASK_EVENTS])

# Start consuming
consumer.consume_events(handle_task_event)
```

## Monitoring

### Kafka UI

-   URL: http://localhost:8080
-   View topics, messages, and consumer groups
-   Monitor message flow and lag

### Command Line Tools

```bash
# List all topics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Describe a topic
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic task-events

# Consume messages from a topic
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic task-events --from-beginning

# Produce a test message
docker exec kafka kafka-console-producer --bootstrap-server localhost:9092 --topic task-events
```

## Integration Examples

### In Manage Task Service

```python
# In main.py
from kafka_events import TaskEventPublisher

# After creating a task
task_publisher = TaskEventPublisher()
task_publisher.publish_task_created(task_data)
task_publisher.close()
```

### In Notify User Service (Future)

```python
# Event handler for notifications
def handle_notification_events(event):
    if event['event_type'] == 'task_created':
        # Send notification to collaborators
        send_notification(event['data'])
```

## Troubleshooting

### Common Issues

1. **Connection Refused**

    - Ensure Kafka is running: `docker-compose ps`
    - Check if ports 9092 and 2181 are available

2. **Topic Not Found**

    - Run the setup script: `docker-compose up kafka-setup`
    - Check if topics exist: `docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list`

3. **Consumer Not Receiving Messages**
    - Check consumer group: `docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list`
    - Reset offset if needed: `docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --reset-offsets --to-earliest --group your-group --topic your-topic --execute`

### Logs

```bash
# View Kafka logs
docker logs kafka

# View Zookeeper logs
docker logs zookeeper

# View setup logs
docker logs kafka-setup
```

## Performance Tuning

### Topic Configuration

-   **Partitions**: 3 (for parallel processing)
-   **Replication Factor**: 1 (for development)
-   **Retention**: 7 days for most topics, 14 days for notifications

### Producer Configuration

-   **Acks**: 'all' (for durability)
-   **Retries**: 3
-   **Batch Size**: Default

### Consumer Configuration

-   **Auto Offset Reset**: 'latest'
-   **Auto Commit**: Enabled
-   **Session Timeout**: Default

## Security Considerations

For production deployment:

1. Enable SASL/SSL authentication
2. Use proper network segmentation
3. Implement topic-level access control
4. Monitor and audit all events
5. Set up proper backup and disaster recovery
