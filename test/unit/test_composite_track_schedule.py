import pytest
from unittest.mock import AsyncMock, Mock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.services.composite.track_schedule import main

pytestmark = pytest.mark.asyncio

# -------------------------------
# /tasks
# -------------------------------
async def test_get_all_tasks_composite_success():
    fake_tasks = {"tasks": [{"id": "33949f99-20d0-423d-9b26-f09292b2e40d", "name": "Task 1"}]}

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json = Mock(return_value=fake_tasks)
        mock_response.raise_for_status = Mock()
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_all_tasks_composite()
        assert result == fake_tasks


async def test_get_all_tasks_composite_failure():
    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("boom")
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        with pytest.raises(main.HTTPException) as e:
            await main.get_all_tasks_composite()
        assert e.value.status_code == 500


# -------------------------------
# /tasks/user/{user_id}
# -------------------------------
async def test_get_tasks_by_user_composite_success():
    user_id = "a1111111-b222-c333-d444-e55555555555"
    fake_user = {"id": user_id, "name": "Alice"}
    fake_tasks = {"tasks": [{"id": "33949f99-20d0-423d-9b26-f09292b2e40d", "collaborators": [user_id], "pid": "p1"}]}
    fake_schedule = {"id": "s1", "task_id": "33949f99-20d0-423d-9b26-f09292b2e40d"}
    fake_project = {"id": "p1", "project": {"name": "Demo"}}

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
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

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
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
# /tasks/project/{project_id}
# -------------------------------
async def test_get_tasks_by_project_composite_success():
    project_id = "p1"
    fake_project = {"id": project_id, "project": {"name": "Demo"}}
    fake_tasks = {"tasks": [{"id": "33949f99-20d0-423d-9b26-f09292b2e40d", "pid": "p1"}]}
    fake_schedule = {"id": "s1", "task_id": "33949f99-20d0-423d-9b26-f09292b2e40d"}

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_project)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_schedule)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_tasks_by_project_composite(project_id)

        assert result["project"]["project"]["name"] == "Demo"
        assert result["count"] == 1
        assert result["tasks"][0]["task"]["id"] == "33949f99-20d0-423d-9b26-f09292b2e40d"


# -------------------------------
# /tasks/{task_id}
# -------------------------------
async def test_get_task_composite_success():
    task_id = "33949f99-20d0-423d-9b26-f09292b2e40d"
    fake_task = {"task": {"id": task_id, "name": "Test Task", "pid": "p1", "created_by_uid": "u1", "collaborators": []}}
    fake_schedule = {"id": "s1"}
    fake_project = {"id": "p1", "project": {"name": "Demo"}}
    fake_user = {"id": "u1", "name": "Alice"}

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
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

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
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
            "schedule": {"status": "todo"}
        }
        result = await main.create_task_composite(payload)

        assert result["message"] == "Task created successfully via composite service"
        assert result["task_id"] == "33949f99-20d0-423d-9b26-f09292b2e40d"
        assert result["schedule"]["status"] == "success"


# -------------------------------
# DELETE /{task_id}
# -------------------------------
async def test_delete_task_composite_success():
    task_id = "33949f99-20d0-423d-9b26-f09292b2e40d"
    fake_schedule_delete = {"deleted": True}
    fake_task_delete = {"deleted": True}

    with patch("backend.services.composite.track_schedule.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.delete.side_effect = [
            AsyncMock(status_code=204, json=Mock(return_value=fake_schedule_delete)),
            AsyncMock(status_code=204, json=Mock(return_value=fake_task_delete)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.delete_task_composite(task_id)

        assert result["task_id"] == task_id
        assert result["message"] == "Delete workflow completed"
        assert "schedule_delete" in result
        assert "task_delete" in result
