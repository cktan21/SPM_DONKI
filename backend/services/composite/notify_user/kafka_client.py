"""
Shared Kafka client utilities for SPM microservices
"""
import json
import logging
import asyncio
from typing import Dict, Any, Optional, Callable
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError
import os
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaEventPublisher:
    """Kafka event publisher for sending events to topics"""
    
    def __init__(self, bootstrap_servers: str = None):
        self.bootstrap_servers = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.producer = None
        self._loop = None
    
    async def _connect(self):
        """Initialize Kafka producer connection"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                request_timeout_ms=30000
            )
            await self.producer.start()
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise
    
    async def publish_event(self, topic: str, event_type: str, data: Dict[str, Any], 
                     key: Optional[str] = None, partition: Optional[int] = None):
        """
        Publish an event to a Kafka topic
        
        Args:
            topic: Kafka topic name
            event_type: Type of event (e.g., 'task_created', 'user_updated')
            data: Event data payload
            key: Optional message key for partitioning
            partition: Optional partition number
        """
        if not self.producer:
            logger.warning("Producer not initialized, attempting to connect...")
            await self._connect()
            if not self.producer:
                logger.error("Failed to initialize producer")
                return False
        
        try:
            event = {
                'event_type': event_type,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'data': data
            }
            
            record_metadata = await self.producer.send_and_wait(
                topic, 
                value=event, 
                key=key,
                partition=partition
            )
            
            logger.info(f"Event published to {topic}: {event_type} at partition {record_metadata.partition}")
            return True
            
        except KafkaError as e:
            logger.error(f"Failed to publish event to {topic}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error publishing event: {e}")
            return False
    
    async def close(self):
        """Close the producer connection"""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer closed")

class KafkaEventConsumer:
    """Kafka event consumer for receiving events from topics"""
    
    def __init__(self, bootstrap_servers: str = None, group_id: str = None):
        self.bootstrap_servers = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.group_id = group_id or os.getenv('KAFKA_GROUP_ID', 'spm-consumer-group')
        self.consumer = None
    
    async def _connect(self):
        """Initialize Kafka consumer connection"""
        try:
            self.consumer = AIOKafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                auto_commit_interval_ms=1000
            )
            await self.consumer.start()
            logger.info(f"Connected to Kafka consumer at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka consumer: {e}")
            raise
    
    async def subscribe_to_topics(self, topics: list):
        """Subscribe to multiple topics"""
        if not self.consumer:
            logger.error("Consumer not initialized")
            return False
        
        try:
            self.consumer.subscribe(topics)
            logger.info(f"Subscribed to topics: {topics}")
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe to topics: {e}")
            return False
    
    async def consume_events(self, handler: Callable[[Dict[str, Any]], None], 
                      timeout_ms: int = 1000):
        """
        Consume events and call handler for each message
        
        Args:
            handler: Function to handle each event
            timeout_ms: Polling timeout in milliseconds
        """
        if not self.consumer:
            logger.error("Consumer not initialized")
            return
        
        try:
            async for message in self.consumer:
                try:
                    event = message.value
                    logger.info(f"Received event: {event.get('event_type')} from {message.topic}")
                    handler(event)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                            
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Error consuming events: {e}")
    
    async def close(self):
        """Close the consumer connection"""
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer closed")

# Event type constants
class EventTypes:
    # Task events
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_ASSIGNED = "task_assigned"
    TASK_STATUS_CHANGED = "task_status_changed"
    
    # # Project events
    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    PROJECT_DELETED = "project_deleted"
    PROJECT_COLLABORATOR_ADDED = "project_collaborator_added"
    PROJECT_COLLABORATOR_REMOVED = "project_collaborator_removed"
    
    # Schedule Events
    SCHEDULE_CREATED = "schedule_created"
    SCHEDULE_UPDATED = "schedule_updated"
    SCHEDULE_DELETED = "schedule_deleted"
    DEADLINE_APPROACHING = "deadline_approaching"
    DEADLINE_OVERDUE = "deadline_overdue"
    
    # User Events
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    
    # Notification Events
    NOTIFICATION_SENT = "notification_sent"
    NOTIFICATION_DELIVERED = "notification_delivered"
    NOTIFICATION_FAILED = "notification_failed"

# Topic constants
class Topics:
    # TASK_EVENTS = "task-events"
    # PROJECT_EVENTS = "project-events"
    # SCHEDULE_EVENTS = "schedule-events"
    # USER_EVENTS = "user-events"
    NOTIFICATION_EVENTS = "notification-events"
