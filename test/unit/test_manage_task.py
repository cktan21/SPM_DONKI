import pytest
from unittest.mock import AsyncMock, Mock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.services.composite.manage_task import main

pytestmark = pytest.mark.asyncio


# -------------------------------
# /tasks/user/{user_id}
# -------------------------------
async def test_get_tasks_by_user_composite_success():
    user_id = "a1111111-b222-c333-d444-e55555555555"
    fake_user = {"id": user_id, "name": "Alice"}
    fake_tasks = {"tasks": [{"id": "33949f99-20d0-423d-9b26-f09292b2e40d", "collaborators": [user_id], "pid": "p1"}]}
    fake_schedule = {"id": "s1", "task_id": "33949f99-20d0-423d-9b26-f09292b2e40d"}
    fake_project = {"id": "p1", "project": {"name": "Demo"}}

    with patch("backend.services.composite.manage_task.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_user)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_schedule)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_project)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_tasks_by_user_composite(user_id)

        assert result["user"]["name"] == "Alice"
        assert result["count"] == 1
        assert result["tasks"][0]["task"]["id"] == "33949f99-20d0-423d-9b26-f09292b2e40d"


async def test_get_tasks_by_user_composite_no_tasks():
    user_id = "a1111111-b222-c333-d444-e55555555555"
    fake_user = {"id": user_id, "name": "Alice"}
    fake_tasks = {"tasks": []}

    with patch("backend.services.composite.manage_task.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_user)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks), raise_for_status=Mock())
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_tasks_by_user_composite(user_id)

        assert result["count"] == 0
        assert result["tasks"] == []


# -------------------------------
# /tasks/tid/{task_id}
# -------------------------------
async def test_get_task_composite_success():
    task_id = "33949f99-20d0-423d-9b26-f09292b2e40d"
    fake_task = {"task": {"id": task_id, "name": "Test Task", "pid": "p1", "created_by_uid": "u1", "collaborators": []}}
    fake_schedule = {"id": "s1"}
    fake_project = {"id": "p1", "project": {"name": "Demo"}}
    fake_user = {"id": "u1", "name": "Alice"}

    with patch("backend.services.composite.manage_task.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_task), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_schedule)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_project)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_user)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_task_composite(task_id)

        assert result["task"]["id"] == task_id
        assert result["task"]["project"]["name"] == "Demo"
        assert result["task"]["created_by"]["name"] == "Alice"


# -------------------------------
# /createTask
# -------------------------------
async def test_create_task_composite_success(monkeypatch):
    fake_task_resp = {"id": "33949f99-20d0-423d-9b26-f09292b2e40d"}
    fake_schedule_resp = {"status": "success", "data": {"id": "s1"}}
    fake_project = {"id": "p1", "project": {"name": "Demo"}}
    fake_user = {"id": "u1", "name": "Alice"}

    async def fake_create_task_service(task_json):
        return fake_task_resp

    async def fake_create_schedule_service(task_id, schedule_data):
        return fake_schedule_resp

    monkeypatch.setattr(main, "create_task_service", fake_create_task_service)
    monkeypatch.setattr(main, "create_schedule_service", fake_create_schedule_service)

    with patch("backend.services.composite.manage_task.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_project)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_user)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        payload = {
            "name": "Test Task",
            "pid": "p1",
            "collaborators": ["u1"],
            "schedule": {"status": "todo", "deadline": "2024-12-31T23:59:59Z"}
        }
        result = await main.create_task_composite(payload)

        assert result["message"] == "Task created successfully via composite service"
        assert result["task_id"] == "33949f99-20d0-423d-9b26-f09292b2e40d"
        assert result["schedule"]["status"] == "success"


async def test_create_task_composite_schedule_validation_error(monkeypatch):
    """Test that schedule validation fails when deadline is missing"""
    
    # Mock the validation functions to avoid network calls
    async def fake_validate_collaborators(collaborators):
        pass
    
    async def fake_validate_project_id(project_id):
        pass
    
    monkeypatch.setattr(main, "validate_collaborators", fake_validate_collaborators)
    monkeypatch.setattr(main, "validate_project_id", fake_validate_project_id)
    
    payload = {
        "name": "Test Task",
        "pid": "p1",
        "collaborators": ["u1"],
        "schedule": {"status": "todo"}  # Missing deadline
    }
    
    with pytest.raises(Exception) as exc_info:
        await main.create_task_composite(payload)
    
    # Check that the error message contains the expected validation error
    assert "Schedule requires 'deadline' field" in str(exc_info.value)


# -------------------------------
# DELETE /{task_id}
# -------------------------------
async def test_delete_task_composite_success():
    task_id = "33949f99-20d0-423d-9b26-f09292b2e40d"
    fake_task_data = {
        "task": {
            "pid": "p1",
            "created_by_uid": "u1", 
            "collaborators": ["u2"]
        }
    }
    fake_task_delete = {"deleted": True}

    with patch("backend.services.composite.manage_task.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        
        # Mock the GET request (to fetch task details)
        mock_get_response = AsyncMock()
        mock_get_response.status_code = 200
        mock_get_response.json = Mock(return_value=fake_task_data)
        mock_client.get.return_value = mock_get_response
        
        # Mock the DELETE request
        mock_delete_response = AsyncMock()
        mock_delete_response.status_code = 204
        mock_delete_response.json = Mock(return_value=fake_task_delete)
        mock_client.delete.return_value = mock_delete_response
        
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.delete_task_composite(task_id)

        assert result["task_id"] == task_id
        assert result["message"] == "Delete workflow completed and project members synced"
        assert "task_delete" in result
        assert "members_sync" in result
        # Verify that only task_delete is present, not schedule_delete
        assert "schedule_delete" not in result
