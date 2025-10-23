# Basic Kafka Commands w `kafka_client.py`

## Publish Events to Kafka

```python
    from kafka_client import KafkaEventPublisher
    publisher = KafkaEventPublisher()
    publisher.publish_event(topic="task-events", event_type="task_created", data=task_data)
    
    # Close Connection if needed
    publisher.close()
```

## Consume Events from Kafka

```python
    from kafka_client import KafkaEventConsumer
    consumer = KafkaEventConsumer()
    consumer.subscribe_to_topics(["task-events"])
    consumer.consume_events(handler=handle_task_event)

    # Close Connection if needed
    consumer.close()
```
