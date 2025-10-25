import requests
import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ScheduleClient:
    def __init__(self, schedule_service_url: str = "http://schedule:5300"):
        self.schedule_service_url = schedule_service_url
        self.session = requests.Session()
        
    def _make_request_with_retry(self, method: str, url: str, max_retries: int = 3, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, timeout=10, **kwargs)
                response.raise_for_status()
                return response
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All {max_retries} attempts failed for {url}")
        return None
        
    def fetch_all_schedules(self) -> List[Dict[str, Any]]:
        """Fetch all schedules from schedule service"""
        response = self._make_request_with_retry("GET", f"{self.schedule_service_url}/all")
        if response:
            data = response.json()
            return data.get("data", [])
        return []
        
    def fetch_recurring_tasks(self) -> List[Dict[str, Any]]:
        """Fetch all recurring tasks from schedule service"""
        response = self._make_request_with_retry("GET", f"{self.schedule_service_url}/recurring/all")
        if response:
            data = response.json()
            return data.get("tasks", [])
        return []
    
    def fetch_schedule_by_sid(self, sid: str) -> Optional[Dict[str, Any]]:
        """Fetch schedule by SID from schedule service"""
        response = self._make_request_with_retry("GET", f"{self.schedule_service_url}/sid/{sid}")
        if response:
            data = response.json()
            return data.get("data")
        return None
    
    def create_schedule(self, tid: str, start: str, deadline: str, is_recurring: bool, 
                       status: str, next_occurrence: str = None, frequency: str = None) -> Optional[Dict[str, Any]]:
        """Create a new schedule entry via schedule service"""
        schedule_data = {
            "tid": tid,
            "start": start,
            "deadline": deadline,
            "is_recurring": is_recurring,
            "status": status,
            "next_occurrence": next_occurrence,
            "frequency": frequency
        }
        
        response = self._make_request_with_retry("POST", f"{self.schedule_service_url}/", json=schedule_data)
        if response:
            data = response.json()
            return data.get("data")
        return None
    
    def update_schedule(self, sid: str, schedule_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a schedule entry via schedule service"""
        response = self._make_request_with_retry("PUT", f"{self.schedule_service_url}/{sid}", json=schedule_data)
        if response:
            return response.json()
        return None
    
    def delete_schedule(self, sid: str) -> Optional[Dict[str, Any]]:
        """Delete a schedule entry via schedule service"""
        response = self._make_request_with_retry("DELETE", f"{self.schedule_service_url}/{sid}")
        if response:
            return response.json()
        return None