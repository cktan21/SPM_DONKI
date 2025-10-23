"""
Kafka event integration for manage-project service
"""
import os
import sys
from typing import Dict, Any
import logging

# Add the shared directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from kafka_client import KafkaEventPublisher, EventTypes, Topics

logger = logging.getLogger(__name__)

class ProjectEventPublisher:
    """Publishes project-related events to Kafka"""
    
    def __init__(self):
        self.publisher = KafkaEventPublisher()
    
    def publish_project_created(self, project_data: Dict[str, Any]):
        """Publish project created event"""
        event_data = {
            'project_id': project_data.get('id'),
            'project_name': project_data.get('name'),
            'owner_id': project_data.get('uid'),
            'description': project_data.get('desc')
        }
        
        self.publisher.publish_event(
            topic=Topics.PROJECT_EVENTS,
            event_type=EventTypes.PROJECT_CREATED,
            data=event_data,
            key=project_data.get('id')
        )
        logger.info(f"Published project created event for project {project_data.get('id')}")
    
    def publish_project_updated(self, project_id: str, updates: Dict[str, Any]):
        """Publish project updated event"""
        event_data = {
            'project_id': project_id,
            'updates': updates,
            'updated_fields': list(updates.keys())
        }
        
        self.publisher.publish_event(
            topic=Topics.PROJECT_EVENTS,
            event_type=EventTypes.PROJECT_UPDATED,
            data=event_data,
            key=project_id
        )
        logger.info(f"Published project updated event for project {project_id}")
    
    def publish_project_deleted(self, project_id: str, project_data: Dict[str, Any]):
        """Publish project deleted event"""
        event_data = {
            'project_id': project_id,
            'project_name': project_data.get('name'),
            'owner_id': project_data.get('uid')
        }
        
        self.publisher.publish_event(
            topic=Topics.PROJECT_EVENTS,
            event_type=EventTypes.PROJECT_DELETED,
            data=event_data,
            key=project_id
        )
        logger.info(f"Published project deleted event for project {project_id}")
    
    def publish_collaborator_added(self, project_id: str, collaborator_id: str, added_by: str):
        """Publish collaborator added event"""
        event_data = {
            'project_id': project_id,
            'collaborator_id': collaborator_id,
            'added_by': added_by
        }
        
        self.publisher.publish_event(
            topic=Topics.PROJECT_EVENTS,
            event_type=EventTypes.PROJECT_COLLABORATOR_ADDED,
            data=event_data,
            key=project_id
        )
        logger.info(f"Published collaborator added event for project {project_id}")
    
    def publish_collaborator_removed(self, project_id: str, collaborator_id: str, removed_by: str):
        """Publish collaborator removed event"""
        event_data = {
            'project_id': project_id,
            'collaborator_id': collaborator_id,
            'removed_by': removed_by
        }
        
        self.publisher.publish_event(
            topic=Topics.PROJECT_EVENTS,
            event_type=EventTypes.PROJECT_COLLABORATOR_REMOVED,
            data=event_data,
            key=project_id
        )
        logger.info(f"Published collaborator removed event for project {project_id}")
    
    def close(self):
        """Close the publisher connection"""
        self.publisher.close()
