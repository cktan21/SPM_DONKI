import pytest
from unittest.mock import AsyncMock, Mock, patch
import os
import sys
from datetime import datetime

# Add the backend path to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, backend_path)

# Mock the problematic modules before any imports
mock_recurring_processor = Mock()
mock_schedule_client = Mock()

# Set up the mock modules
sys.modules['recurring_processor'] = mock_recurring_processor
sys.modules['schedule_client'] = mock_schedule_client

# Import the modules
from backend.services.composite.notify_user import main

# pytestmark = pytest.mark.asyncio  # Not needed for synchronous tests


class TestScheduleNotifyIntegration:
    """Test the integration between schedule service and notify_user service"""
    
    def test_schedule_new_recurring_task_success(self):
        """Test successful scheduling of a new recurring task"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        task_data = {
            "sid": "s123",
            "tid": "t456", 
            "frequency": "Weekly",
            "next_occurrence": "2024-01-08T09:00:00Z",
            "start": "2024-01-01T09:00:00Z",
            "deadline": "2024-01-03T17:00:00Z",
            "status": "ongoing"
        }
        
        with patch.object(main.recurring_processor, 'schedule_recurring_task', return_value=True):
            response = client.post("/task/recurring/schedule", json=task_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Successfully scheduled recurring task s123"
            assert data["sid"] == "s123"
            assert data["frequency"] == "Weekly"
            assert data["next_occurrence"] == "2024-01-08T09:00:00Z"

    def test_schedule_new_recurring_task_missing_fields(self):
        """Test error handling when required fields are missing"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        # Missing frequency
        task_data = {
            "sid": "s123",
            "tid": "t456",
            "next_occurrence": "2024-01-08T09:00:00Z"
        }
        
        response = client.post("/task/recurring/schedule", json=task_data)
        
        # The error is caught and returns 500 due to the exception handling
        assert response.status_code == 500
        assert "Error scheduling recurring task" in response.json()["detail"]

    def test_schedule_new_recurring_task_scheduling_failure(self):
        """Test error handling when scheduling fails"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        task_data = {
            "sid": "s123",
            "tid": "t456",
            "frequency": "Weekly",
            "next_occurrence": "2024-01-08T09:00:00Z"
        }
        
        with patch.object(main.recurring_processor, 'schedule_recurring_task', return_value=False):
            response = client.post("/task/recurring/schedule", json=task_data)
            
            assert response.status_code == 500
            assert "Failed to schedule recurring task" in response.json()["detail"]

    def test_schedule_new_recurring_task_invalid_datetime(self):
        """Test error handling with invalid datetime format"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        task_data = {
            "sid": "s123",
            "tid": "t456",
            "frequency": "Weekly",
            "next_occurrence": "invalid-datetime"
        }
        
        response = client.post("/task/recurring/schedule", json=task_data)
        
        assert response.status_code == 500
        assert "Error scheduling recurring task" in response.json()["detail"]
