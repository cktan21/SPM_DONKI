import pytest
from unittest.mock import AsyncMock, Mock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.services.composite.manage_project import main

pytestmark = pytest.mark.asyncio

# -------------------------------
# /uid/{uid}
# -------------------------------
async def test_get_project_with_tasks_success():
    fake_projects = {
        "project": [
            {"id": "p1", "name": "Project Alpha", "desc": "First project"},
            {"id": "p2", "name": "Project Beta", "desc": "Second project"}
        ]
    }
    fake_tasks = {"tasks": [{"id": "t1", "name": "Task 1", "pid": "p1"}]}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_projects), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks)),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks)),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project_with_tasks("user-123")

        assert result["message"] == "Projects retrieved successfully"
        assert result["user_id"] == "user-123"
        assert len(result["projects"]) == 2
        assert result["projects"][0]["id"] == "p1"
        assert result["projects"][0]["name"] == "Project Alpha"
        assert "tasks" in result["projects"][0]


async def test_get_project_with_tasks_no_projects():
    fake_projects = {"project": []}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = AsyncMock(
            status_code=200, 
            json=Mock(return_value=fake_projects), 
            raise_for_status=Mock()
        )
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project_with_tasks("user-123")

        assert result["message"] == "No projects found for this user"
        assert result["user_id"] == "user-123"
        assert result["projects"] == []


async def test_get_project_with_tasks_service_error():
    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Service error")
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        with pytest.raises(main.HTTPException) as e:
            await main.get_project_with_tasks("user-123")
        assert e.value.status_code == 500


# -------------------------------
# /pid/{project_id}
# -------------------------------
async def test_get_project_success():
    fake_project = {"project": {"id": "p1", "name": "Project Alpha", "desc": "First project"}}
    fake_tasks = {"tasks": [{"id": "t1", "name": "Task 1", "pid": "p1"}]}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_project), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks), raise_for_status=Mock()),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project("p1")

        assert result["message"] == "Project retrieved successfully"
        assert result["project_id"] == "p1"
        assert result["project"]["id"] == "p1"
        assert result["project"]["name"] == "Project Alpha"
        assert "tasks" in result["project"]
        assert len(result["project"]["tasks"]) == 1


async def test_get_project_not_found():
    fake_project = {"project": []}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = AsyncMock(
            status_code=200, 
            json=Mock(return_value=fake_project), 
            raise_for_status=Mock()
        )
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project("p1")

        assert result["message"] == "No projects found for this user"
        assert result["project_id"] == "p1"
        assert result["project"] is None


async def test_get_project_with_tasks_success():
    """Test successful retrieval of single project with tasks"""
    fake_project = {"project": {"id": "p1", "name": "Project Alpha", "desc": "First project"}}
    fake_tasks = {"tasks": [{"id": "t1", "name": "Task 1", "pid": "p1"}]}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = [
            AsyncMock(status_code=200, json=Mock(return_value=fake_project), raise_for_status=Mock()),
            AsyncMock(status_code=200, json=Mock(return_value=fake_tasks), raise_for_status=Mock()),
        ]
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project("p1")

        assert result["message"] == "Project retrieved successfully"
        assert result["project_id"] == "p1"
        assert result["project"]["id"] == "p1"
        assert result["project"]["name"] == "Project Alpha"
        assert "tasks" in result["project"]
        assert len(result["project"]["tasks"]) == 1


# -------------------------------
# Error handling tests
# -------------------------------
async def test_concurrent_task_fetching():
    """Test that task fetching happens concurrently"""
    fake_projects = {
        "project": [
            {"id": "p1", "name": "Project 1"},
            {"id": "p2", "name": "Project 2"}
        ]
    }
    fake_tasks = {"tasks": [{"id": "t1", "name": "Task 1"}]}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        
        # Track the order of calls
        call_order = []
        
        async def mock_get(url, **kwargs):
            call_order.append(url)
            if "uid" in url:
                return AsyncMock(
                    status_code=200, 
                    json=Mock(return_value=fake_projects), 
                    raise_for_status=Mock()
                )
            else:
                return AsyncMock(
                    status_code=200, 
                    json=Mock(return_value=fake_tasks)
                )
        
        mock_client.get.side_effect = mock_get
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project_with_tasks("user-123")

        assert result["message"] == "Projects retrieved successfully"
        assert len(result["projects"]) == 2
        # Verify that project service was called first
        assert "uid" in call_order[0]


async def test_malformed_response_handling():
    """Test handling of malformed responses"""
    fake_projects = {"invalid": "structure"}

    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = AsyncMock(
            status_code=200, 
            json=Mock(return_value=fake_projects), 
            raise_for_status=Mock()
        )
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        result = await main.get_project_with_tasks("user-123")

        assert result["message"] == "No projects found for this user"
        assert result["projects"] == []


async def test_network_error_handling():
    """Test network error handling"""
    with patch("backend.services.composite.manage_project.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.side_effect = main.httpx.RequestError("Network error")
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        with pytest.raises(main.HTTPException) as e:
            await main.get_project_with_tasks("user-123")
        assert e.value.status_code == 503
        assert "Project service unavailable" in str(e.value.detail)
