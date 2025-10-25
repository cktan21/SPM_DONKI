import requests
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ScheduleClient:
    def __init__(self, schedule_service_url: str = "http://schedule:5300"):
        self.schedule_service_url = schedule_service_url
        self.session = requests.Session()
        
    def fetch_all_schedules(self) -> List[Dict[str, Any]]:
        """Fetch all schedules from schedule service"""
        try:
            response = self.session.get(f"{self.schedule_service_url}/all")
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            logger.error(f"Error fetching all schedules: {str(e)}")
        
    def fetch_recurring_tasks(self) -> List[Dict[str, Any]]:
        """Fetch all recurring tasks from schedule service"""
        try:
            response = self.session.get(f"{self.schedule_service_url}/recurring/all")
            response.raise_for_status()
            data = response.json()
            return data.get("tasks", [])
        except Exception as e:
            logger.error(f"Error fetching recurring tasks: {str(e)}")
            return []
    
    def fetch_schedule_by_sid(self, sid: str) -> Optional[Dict[str, Any]]:
        """Fetch schedule by SID from schedule service"""
        try:
            response = self.session.get(f"{self.schedule_service_url}/sid/{sid}")
            response.raise_for_status()
            data = response.json()
            return data.get("data")
        except Exception as e:
            logger.error(f"Error fetching schedule {sid}: {str(e)}")
            return None
    
    def create_schedule(self, tid: str, start: str, deadline: str, is_recurring: bool, 
                       status: str, next_occurrence: str = None, frequency: str = None) -> Optional[Dict[str, Any]]:
        """Create a new schedule entry via schedule service"""
        try:
            schedule_data = {
                "tid": tid,
                "start": start,
                "deadline": deadline,
                "is_recurring": is_recurring,
                "status": status,
                "next_occurrence": next_occurrence,
                "frequency": frequency
            }
            
            response = self.session.post(
                f"{self.schedule_service_url}/",
                json=schedule_data
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data")
        except Exception as e:
            logger.error(f"Error creating schedule: {str(e)}")
            return None
    
    def update_schedule(self, sid: str, schedule_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a schedule entry via schedule service"""
        try:
            response = self.session.put(f"{self.schedule_service_url}/{sid}", json=schedule_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error updating schedule {sid}: {str(e)}")
            return None
    
    def delete_schedule(self, sid: str) -> Optional[Dict[str, Any]]:
        """Delete a schedule entry via schedule service"""
        try:
            response = self.session.delete(f"{self.schedule_service_url}/{sid}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error deleting schedule {sid}: {str(e)}")
            return None