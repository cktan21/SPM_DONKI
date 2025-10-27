#!/usr/bin/env python3
"""
Schedule Client
This module provides a client for interacting with the schedule service
"""

import requests
import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ScheduleClient:
    def __init__(self, schedule_service_url: str = "http://schedule:5300", task_service_url: str = "http://tasks:5500", user_service_url: str = "http://user:5100"):
        self.schedule_service_url = schedule_service_url
        self.task_service_url = task_service_url
        self.user_service_url = user_service_url
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
    
    def update_schedule(self, sid: str, schedule_data: Dict[str, Any]) -> bool:
        """Update a schedule entry via schedule service"""
        logger.info(f"Updating schedule {sid} with data: {schedule_data}")
        response = self._make_request_with_retry("PUT", f"{self.schedule_service_url}/{sid}", json=schedule_data)
        if response:
            try:
                response_data = response.json()
                logger.info(f"Schedule update response: {response_data}")
                return response_data is not None
            except Exception as e:
                logger.error(f"Error parsing response from schedule service: {e}")
                return False
        else:
            logger.error(f"Failed to get response from schedule service for sid {sid}")
        return False
    
    def delete_schedule(self, sid: str) -> Optional[Dict[str, Any]]:
        """Delete a schedule entry via schedule service"""
        response = self._make_request_with_retry("DELETE", f"{self.schedule_service_url}/{sid}")
        if response:
            return response.json()
        return None
    
    def get_user_info_old(self, sid: str) -> Optional[List[Dict[str, Any]]]:
        """Get task info by SID from schedule service"""
        try:
            schedule_response = self._make_request_with_retry("GET", f"{self.schedule_service_url}/sid/{sid}")
            if not schedule_response:
                logger.error(f"Failed to get schedule for sid {sid}")
                return None
                
            schedule_data = schedule_response.json().get("data")
            if not schedule_data:
                logger.error(f"No schedule data found for sid {sid}")
                return None
                
            tid = schedule_data.get("tid")
            if not tid:
                logger.error(f"No tid found in schedule data for sid {sid}")
                return None
                
            logger.info(f"Getting task info for tid {tid}")
            task_response = self._make_request_with_retry("GET", f"{self.task_service_url}/tid/{tid}")
            if not task_response:
                logger.error(f"Failed to get task info for tid {tid}")
                return None
                
            task_data = task_response.json().get("task")
            if not task_data:
                logger.error(f"No task data found for tid {tid}")
                return None
                
            collaborators = task_data.get("collaborators", [])
            created_by_uid = task_data.get("created_by_uid")
            
            # Combine collaborators and creator
            user_ids = collaborators.copy()
            if created_by_uid and created_by_uid not in user_ids:
                user_ids.append(created_by_uid)
                
            if not user_ids:
                logger.error(f"No user IDs found for task {tid}")
                return None
                
            logger.info(f"Getting user info for user IDs: {user_ids}")
            user_response = self._make_request_with_retry("GET", f"{self.user_service_url}/user", params={"uid": user_ids})
            if user_response:
                data = user_response.json()
                return data.get("users", [])
            else:
                logger.error(f"Failed to get user info for user IDs: {user_ids}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user info for sid {sid}: {str(e)}")
            return None
        
    def get_user_info(self, sid: str) -> Optional[List[Dict[str, Any]]]:
        """Get task info by SID from schedule service"""
        try:
            response = self._make_request_with_retry("GET", f"{self.schedule_service_url}/user-info/sid/{sid}")
            if response:
                data = response.json()
                return data.get("data")
            return None
            
        except Exception as e:
            logger.error(f"Error getting user info for sid {sid}: {str(e)}")
            return None