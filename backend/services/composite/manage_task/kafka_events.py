"""
Kafka event integration for manage-task service
"""
import os
import sys
from typing import Dict, Any
import logging

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from kafka_client import KafkaEventPublisher, EventTypes, Topics

logger = logging.getLogger(__name__)

class TaskEventPublisher:
    """Publishes task-related events to Kafka"""
    
    def __init__(self):
        self.publisher = KafkaEventPublisher()
    
    def publish_task_created(self, task_data: Dict[str, Any]):
        """Publish task created event"""
        event_data = {
            'task_id': task_data.get('id'),
            'task_name': task_data.get('name'),
            'created_by': task_data.get('created_by_uid'),
            'project_id': task_data.get('pid'),
            'collaborators': task_data.get('collaborators', []),
            'parent_task_id': task_data.get('parentTaskId')
        }
        
        self.publisher.publish_event(
            topic=Topics.TASK_EVENTS,
            event_type=EventTypes.TASK_CREATED,
            data=event_data,
            key=task_data.get('id')
        )
        logger.info(f"Published task created event for task {task_data.get('id')}")
    
    def publish_task_updated(self, task_id: str, updates: Dict[str, Any]):
        """Publish task updated event"""
        event_data = {
            'task_id': task_id,
            'updates': updates,
            'updated_fields': list(updates.keys())
        }
        
        self.publisher.publish_event(
            topic=Topics.TASK_EVENTS,
            event_type=EventTypes.TASK_UPDATED,
            data=event_data,
            key=task_id
        )
        logger.info(f"Published task updated event for task {task_id}")
    
    def publish_task_deleted(self, task_id: str, task_data: Dict[str, Any]):
        """Publish task deleted event"""
        event_data = {
            'task_id': task_id,
            'task_name': task_data.get('name'),
            'project_id': task_data.get('pid'),
            'collaborators': task_data.get('collaborators', [])
        }
        
        self.publisher.publish_event(
            topic=Topics.TASK_EVENTS,
            event_type=EventTypes.TASK_DELETED,
            data=event_data,
            key=task_id
        )
        logger.info(f"Published task deleted event for task {task_id}")
    
    def publish_task_assigned(self, task_id: str, assignee_id: str, assigned_by: str):
        """Publish task assigned event"""
        event_data = {
            'task_id': task_id,
            'assignee_id': assignee_id,
            'assigned_by': assigned_by
        }
        
        self.publisher.publish_event(
            topic=Topics.TASK_EVENTS,
            event_type=EventTypes.TASK_ASSIGNED,
            data=event_data,
            key=task_id
        )
        logger.info(f"Published task assigned event for task {task_id}")
    
    def publish_task_status_changed(self, task_id: str, old_status: str, new_status: str):
        """Publish task status changed event"""
        event_data = {
            'task_id': task_id,
            'old_status': old_status,
            'new_status': new_status
        }
        
        self.publisher.publish_event(
            topic=Topics.TASK_EVENTS,
            event_type=EventTypes.TASK_STATUS_CHANGED,
            data=event_data,
            key=task_id
        )
        logger.info(f"Published task status changed event for task {task_id}")
    
    def close(self):
        """Close the publisher connection"""
        self.publisher.close()
