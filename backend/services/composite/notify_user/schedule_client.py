import requests
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ScheduleClient:
    def __init__(self, schedule_service_url: str = "http://schedule:5300"):
        self.schedule_service_url = schedule_service_url
        self.session = requests.Session()
        
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
