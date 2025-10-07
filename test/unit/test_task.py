import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.tasks.supabaseClient import SupabaseClient


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def mock_client():
    """Patch create_client and return a mocked Supabase client."""
    with patch("backend.services.atomic.tasks.supabaseClient.create_client") as mock_create_client:
        client = MagicMock()
        mock_create_client.return_value = client
        yield client


@pytest.fixture
def supabase_client(mock_client):
    """Return SupabaseClient with mocked client."""
    return SupabaseClient()


# -------------------------------
# Helper functions
# -------------------------------
def sample_create_payload(**overrides) -> Dict[str, Any]:
    payload = {
        "name": "New Task Title",
        "desc": "Optional description",
        "notes": "Optional notes",
        "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
    }
    payload.update(overrides)
    return payload


def sample_update_payload(**overrides) -> Dict[str, Any]:
    payload = {
        "name": "Complete Project Setup",
        "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
        "collaborators": [
            "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
            "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002",
        ],
        "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
        "desc": "Set up the initial project structure and dependencies",
        "notes": "Remember to update the README file",
    }
    payload.update(overrides)
    return payload


# -------------------------------
# Get All Tasks tests
# -------------------------------
def test_get_all_tasks_success(mock_client, supabase_client):
    """Test successful retrieval of all tasks"""
    expected_tasks = [
        {"id": "task1", "name": "Task 1"},
        {"id": "task2", "name": "Task 2"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = expected_tasks
    
    result = supabase_client.get_all_tasks()
    
    mock_client.table.assert_called_once_with("TASK")
    mock_table.select.assert_called_once_with("*")
    assert result == expected_tasks


def test_get_all_tasks_empty(mock_client, supabase_client):
    """Test get_all_tasks when no tasks exist"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = []
    
    result = supabase_client.get_all_tasks()
    
    assert result == []


def test_get_all_tasks_with_filter(mock_client, supabase_client):
    """Test get_all_tasks with filter parameters"""
    filter_by = {"created_by_uid": "user123"}
    expected_tasks = [{"id": "task1", "created_by_uid": "user123"}]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected_tasks
    
    result = supabase_client.get_all_tasks(filter_by)
    
    mock_table.select.return_value.eq.assert_called_once_with("created_by_uid", "user123")
    assert result == expected_tasks


# -------------------------------
# Update Task tests
# -------------------------------
def test_update_task_success(mock_client, supabase_client):
    """Test successful task update"""
    task_id = "task123"
    updates = {"name": "Updated Task", "desc": "Updated description"}
    updated_task = {"id": task_id, "name": "Updated Task", "desc": "Updated description"}
    
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated_task]
    
    result = supabase_client.update_task(task_id, updates)
    
    mock_client.table.assert_called_once_with("TASK")
    mock_table.update.assert_called_once_with(updates)
    mock_table.update.return_value.eq.assert_called_once_with("id", task_id)
    assert result.data == [updated_task]


def test_update_task_not_found(mock_client, supabase_client):
    """Test update task when task doesn't exist"""
    task_id = "nonexistent"
    updates = {"name": "Updated Task"}
    
    mock_table = mock_client.table.return_value
    # Mock the update to return empty data, which triggers the fetch logic
    mock_table.update.return_value.eq.return_value.execute.return_value.data = []
    # Mock the subsequent fetch to also return empty data
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    
    result = supabase_client.update_task(task_id, updates)
    
    # Verify both update and select were called
    mock_table.update.assert_called_once_with(updates)
    mock_table.select.assert_called_once_with("*")
    assert result.data == []


# -------------------------------
# Delete Task tests
# -------------------------------
def test_delete_task_success(mock_client, supabase_client):
    """Test successful task deletion"""
    task_id = "task123"
    deleted_task = {"id": task_id, "name": "Deleted Task"}
    
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [deleted_task]
    
    result = supabase_client.delete_task(task_id)
    
    mock_client.table.assert_called_once_with("TASK")
    mock_table.delete.return_value.eq.assert_called_once_with("id", task_id)
    assert result.data == [deleted_task]


def test_delete_task_not_found(mock_client, supabase_client):
    """Test delete task when task doesn't exist"""
    task_id = "nonexistent"
    
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = []
    
    result = supabase_client.delete_task(task_id)
    
    assert result.data == []