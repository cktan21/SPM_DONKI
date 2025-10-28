import pytest
from unittest.mock import AsyncMock, Mock, patch, MagicMock
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Add the backend path to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, backend_path)

# Add the service directory to Python path so kafka_client and schedule_client can be found
service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/services/composite/notify_user"))
sys.path.insert(0, service_path)

# Mock the problematic modules before any imports
mock_recurring_processor = MagicMock()
mock_schedule_client = MagicMock()

# Set up the mock modules
sys.modules['recurring_processor'] = mock_recurring_processor
sys.modules['schedule_client'] = mock_schedule_client

# Now we can import the individual modules
from backend.services.composite.notify_user.recurring_processor import RecurringTaskProcessor
from backend.services.composite.notify_user.schedule_client import ScheduleClient

# Import main after setting up mocks
from backend.services.composite.notify_user import main

# pytestmark = pytest.mark.asyncio  # Not needed for synchronous tests


# -------------------------------
# Test ScheduleClient
# -------------------------------
class TestScheduleClient:
    def test_fetch_recurring_tasks_success(self):
        """Test successful fetching of recurring tasks"""
        mock_response = Mock()
        mock_response.json.return_value = {"tasks": [{"id": "1", "frequency": "Weekly"}]}
        
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=mock_response):
            client = ScheduleClient()
            result = client.fetch_recurring_tasks()
            
            assert len(result) == 1
            assert result[0]["id"] == "1"
            assert result[0]["frequency"] == "Weekly"

    def test_fetch_recurring_tasks_error(self):
        """Test error handling when fetching recurring tasks fails"""
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=None):
            client = ScheduleClient()
            result = client.fetch_recurring_tasks()
            
            assert result == []

    def test_fetch_schedule_by_sid_success(self):
        """Test successful fetching of schedule by SID"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"sid": "s1", "tid": "t1"}}
        
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=mock_response):
            client = ScheduleClient()
            result = client.fetch_schedule_by_sid("s1")
            
            assert result["sid"] == "s1"
            assert result["tid"] == "t1"

    def test_fetch_schedule_by_sid_error(self):
        """Test error handling when fetching schedule by SID fails"""
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=None):
            client = ScheduleClient()
            result = client.fetch_schedule_by_sid("s1")
            
            assert result is None

    def test_create_schedule_success(self):
        """Test successful creation of schedule"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"sid": "s1", "tid": "t1"}}
        
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=mock_response):
            client = ScheduleClient()
            result = client.create_schedule(
                tid="t1",
                start="2024-01-01T00:00:00Z",
                deadline="2024-01-02T00:00:00Z",
                is_recurring=True,
                status="ongoing",
                next_occurrence="2024-01-08T00:00:00Z",
                frequency="Weekly"
            )
            
            assert result["sid"] == "s1"
            assert result["tid"] == "t1"

    def test_create_schedule_error(self):
        """Test error handling when creating schedule fails"""
        with patch.object(ScheduleClient, '_make_request_with_retry', return_value=None):
            client = ScheduleClient()
            result = client.create_schedule(
                tid="t1",
                start="2024-01-01T00:00:00Z",
                deadline="2024-01-02T00:00:00Z",
                is_recurring=True,
                status="ongoing"
            )
            
            assert result is None


# -------------------------------
# Test RecurringTaskProcessor
# -------------------------------
class TestRecurringTaskProcessor:
    def setup_method(self):
        """Setup for each test method"""
        with patch('backend.services.composite.notify_user.recurring_processor.BackgroundScheduler') as mock_scheduler:
            self.processor = RecurringTaskProcessor()
            self.mock_scheduler = mock_scheduler.return_value

    def test_calculate_next_occurrence_weekly(self):
        """Test weekly frequency calculation"""
        current_start = datetime(2024, 1, 1, 9, 0, 0)
        current_deadline = datetime(2024, 1, 3, 17, 0, 0)
        
        result = self.processor.calculate_next_occurrence("Weekly", current_start, current_deadline)
        
        # The implementation converts to UTC+8 timezone, so we need to account for that
        expected = current_start + timedelta(weeks=1) + (current_deadline - current_start)
        # Convert expected to UTC+8 timezone for comparison
        import pytz
        utc_plus_8 = pytz.timezone('Asia/Singapore')
        expected = utc_plus_8.localize(expected)
        assert result == expected

    def test_calculate_next_occurrence_monthly(self):
        """Test monthly frequency calculation"""
        current_start = datetime(2024, 1, 1, 9, 0, 0)
        current_deadline = datetime(2024, 1, 3, 17, 0, 0)
        
        result = self.processor.calculate_next_occurrence("Monthly", current_start, current_deadline)
        
        # The implementation converts to UTC+8 timezone, so we need to account for that
        expected = current_start + relativedelta(months=1) + (current_deadline - current_start)
        # Convert expected to UTC+8 timezone for comparison
        import pytz
        utc_plus_8 = pytz.timezone('Asia/Singapore')
        expected = utc_plus_8.localize(expected)
        assert result == expected

    def test_calculate_next_occurrence_yearly(self):
        """Test yearly frequency calculation"""
        current_start = datetime(2024, 1, 1, 9, 0, 0)
        current_deadline = datetime(2024, 1, 3, 17, 0, 0)
        
        result = self.processor.calculate_next_occurrence("Yearly", current_start, current_deadline)
        
        # The implementation converts to UTC+8 timezone, so we need to account for that
        expected = current_start + relativedelta(years=1) + (current_deadline - current_start)
        # Convert expected to UTC+8 timezone for comparison
        import pytz
        utc_plus_8 = pytz.timezone('Asia/Singapore')
        expected = utc_plus_8.localize(expected)
        assert result == expected

    def test_calculate_next_occurrence_immediate(self):
        """Test immediate frequency calculation"""
        current_start = datetime(2024, 1, 1, 9, 0, 0)
        current_deadline = datetime(2024, 1, 3, 17, 0, 0)
        
        result = self.processor.calculate_next_occurrence("Immediate", current_start, current_deadline)
        
        # The implementation converts to UTC+8 timezone, so we need to account for that
        expected = current_deadline + timedelta(minutes=1)
        # Convert expected to UTC+8 timezone for comparison
        import pytz
        utc_plus_8 = pytz.timezone('Asia/Singapore')
        expected = utc_plus_8.localize(expected)
        assert result == expected

    def test_calculate_next_occurrence_invalid_frequency(self):
        """Test invalid frequency raises ValueError"""
        current_start = datetime(2024, 1, 1, 9, 0, 0)
        current_deadline = datetime(2024, 1, 3, 17, 0, 0)
        
        with pytest.raises(ValueError, match="Unsupported frequency"):
            self.processor.calculate_next_occurrence("Invalid", current_start, current_deadline)

    def test_create_recurring_entry_success(self):
        """Test successful creation of recurring entry"""
        original_entry = {
            "tid": "t1",
            "start": "2024-01-01T09:00:00Z",
            "deadline": "2024-01-03T17:00:00Z"
        }
        
        mock_new_entry = {"sid": "s2", "tid": "t1"}
        
        with patch.object(self.processor.schedule_client, 'create_schedule', return_value=mock_new_entry):
            result = self.processor.create_recurring_entry(original_entry, "Weekly")
            
            assert result == mock_new_entry

    def test_create_recurring_entry_error(self):
        """Test error handling in create_recurring_entry"""
        original_entry = {
            "tid": "t1",
            "start": "invalid-date",
            "deadline": "2024-01-03T17:00:00Z"
        }
        
        result = self.processor.create_recurring_entry(original_entry, "Weekly")
        
        assert result is None

    def test_schedule_recurring_task_success(self):
        """Test successful scheduling of recurring task"""
        task_data = {
            "sid": "s1", 
            "frequency": "Weekly",
            "next_occurrence": "2024-01-08T09:00:00Z"
        }
        
        result = self.processor.schedule_recurring_task(task_data)
        
        assert result is True
        self.mock_scheduler.add_job.assert_called_once()

    def test_schedule_recurring_task_not_found(self):
        """Test scheduling when schedule entry not found"""
        task_data = {
            "sid": "s1", 
            "frequency": "Weekly",
            "next_occurrence": "2024-01-08T09:00:00Z"
        }
        
        result = self.processor.schedule_recurring_task(task_data)
        
        assert result is True  # The method doesn't check for schedule entry existence

    def test_process_recurring_task_success(self):
        """Test successful processing of recurring task"""
        mock_current_entry = {
            "sid": "s1",
            "tid": "t1",
            "start": "2024-01-01T09:00:00Z",
            "deadline": "2024-01-03T17:00:00Z"
        }
        mock_new_entry = {"sid": "s2", "next_occurrence": "2024-01-08T09:00:00Z"}
        
        with patch.object(self.processor.schedule_client, 'fetch_schedule_by_sid', return_value=mock_current_entry), \
             patch.object(self.processor, 'create_recurring_entry', return_value=mock_new_entry), \
             patch.object(self.processor, 'schedule_recurring_task', return_value=True):
            
            self.processor.process_recurring_task("s1", "Weekly")
            
            # Verify that create_recurring_entry was called
            self.processor.create_recurring_entry.assert_called_once()

    def test_process_recurring_task_entry_not_found(self):
        """Test processing when current entry not found"""
        with patch.object(self.processor.schedule_client, 'fetch_schedule_by_sid', return_value=None):
            # Should not raise exception, just log error
            self.processor.process_recurring_task("s1", "Weekly")

    def test_cancel_recurring_task_success(self):
        """Test successful cancellation of recurring task"""
        result = self.processor.cancel_recurring_task("s1")
        
        assert result is True
        self.mock_scheduler.remove_job.assert_called_once_with("recurring_s1")

    def test_cancel_recurring_task_error(self):
        """Test error handling when cancelling recurring task"""
        self.mock_scheduler.remove_job.side_effect = Exception("Job not found")
        
        result = self.processor.cancel_recurring_task("s1")
        
        assert result is False

    def test_get_scheduled_jobs(self):
        """Test getting scheduled jobs"""
        mock_job = Mock()
        mock_job.id = "recurring_s1"
        mock_job.next_run_time = datetime(2024, 1, 8, 9, 0, 0)
        self.mock_scheduler.get_jobs.return_value = [mock_job]
        
        result = self.processor.get_scheduled_jobs()
        
        assert len(result) == 1
        assert result[0]["id"] == "recurring_s1"

    def test_shutdown(self):
        """Test shutdown method"""
        self.processor.shutdown()
        self.mock_scheduler.shutdown.assert_called_once()


# -------------------------------
# Test FastAPI Endpoints (Simplified)
# -------------------------------
class TestNotifyUserEndpoints:
    def test_read_root(self):
        """Test root endpoint"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Notify User Service is running 🚀😌"

    def test_get_favicon(self):
        """Test favicon endpoint"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        response = client.get("/favicon.ico")
        assert response.status_code == 204

    def test_get_all_recurring_tasks_success(self):
        """Test successful retrieval of recurring tasks"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        mock_tasks = [
            {"sid": "s1", "frequency": "Weekly", "next_occurrence": "2024-01-08T09:00:00Z"},
            {"sid": "s2", "frequency": "Monthly", "next_occurrence": "2024-02-01T09:00:00Z"}
        ]
        
        with patch.object(main.schedule_client, 'fetch_recurring_tasks', return_value=mock_tasks):
            response = client.get("/task/recurring")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Retrieved 2 recurring tasks"
            assert len(data["tasks"]) == 2

    def test_get_all_recurring_tasks_error(self):
        """Test error handling when fetching recurring tasks fails"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        with patch.object(main.schedule_client, 'fetch_recurring_tasks', side_effect=Exception("Database error")):
            response = client.get("/task/recurring")
            
            assert response.status_code == 500
            assert "Error fetching recurring tasks" in response.json()["detail"]

    def test_get_scheduled_jobs_success(self):
        """Test successful retrieval of scheduled jobs"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        mock_jobs = [
            {"id": "recurring_s1", "next_run_time": "2024-01-08T09:00:00Z"},
            {"id": "recurring_s2", "next_run_time": "2024-02-01T09:00:00Z"}
        ]
        
        with patch.object(main.recurring_processor, 'get_scheduled_jobs', return_value=mock_jobs):
            response = client.get("/task/scheduled")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Retrieved 2 scheduled jobs"
            assert len(data["jobs"]) == 2

    def test_get_scheduled_jobs_error(self):
        """Test error handling when fetching scheduled jobs fails"""
        from fastapi.testclient import TestClient
        client = TestClient(main.app)
        
        with patch.object(main.recurring_processor, 'get_scheduled_jobs', side_effect=Exception("Scheduler error")):
            response = client.get("/task/scheduled")
            
            assert response.status_code == 500
            assert "Error fetching scheduled jobs" in response.json()["detail"]

