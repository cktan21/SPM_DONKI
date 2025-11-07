import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call
from fastapi.testclient import TestClient
from starlette.testclient import TestClient as _TC
from fastapi import HTTPException

# Make repo root importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.project.services.supabaseClient import SupabaseClient

# ======================================================================
#                           SupabaseClient tests
# ======================================================================

@pytest.fixture
def mock_client():
    with patch("backend.services.atomic.project.services.supabaseClient.create_client") as mock_create_client:
        client = MagicMock()
        mock_create_client.return_value = client
        yield client

@pytest.fixture
def supabase_client(mock_client):
    return SupabaseClient()

# -------------------------------
# insert_project tests
# -------------------------------
def test_insert_project_success(mock_client, supabase_client):
    uid = "user-123"
    name = "New Project"
    desc = "Project Description"
    members = ["user-123", "user-456"]
    expected = {
        "id": "project-1",
        "uid": uid,
        "name": name,
        "desc": desc,
        "members": members,
        "department": "ENG",
        "created_at": "2025-11-01T00:00:00Z",
        "updated_at": "2025-11-01T00:00:00Z",
    }

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [expected]

    result = supabase_client.insert_project(uid, name, desc, members)

    mock_client.table.assert_called_once_with("PROJECT")
    mock_table.insert.assert_called_once_with({
        "uid": uid,
        "name": name,
        "desc": desc,
        "members": members
    })
    assert result["id"] == expected["id"]
    assert result["uid"] == uid
    assert result["name"] == name
    assert result["members"] == members
    assert "department" in result

def test_insert_project_without_description(mock_client, supabase_client):
    uid = "user-123"
    name = "Simple Project"
    desc = None
    members = ["user-123"]

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {"id": "project-1", "uid": uid, "name": name, "desc": None, "members": members}
    ]

    result = supabase_client.insert_project(uid, name, desc, members)

    mock_table.insert.assert_called_once_with({
        "uid": uid,
        "name": name,
        "desc": desc,
        "members": members
    })
    assert result["name"] == name
    assert result["desc"] is None
    assert result["members"] == members

def test_insert_project_empty_result(mock_client, supabase_client):
    uid, name, desc, members = "user123", "My Project", "Description", ["user123"]
    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = []
    result = supabase_client.insert_project(uid, name, desc, members)
    assert result is None

def test_insert_project_failure_raises(mock_client, supabase_client):
    uid, name, desc, members = "user123", "My Project", "Description", ["user123"]
    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.side_effect = Exception("Insert failed")
    with pytest.raises(Exception):
        supabase_client.insert_project(uid, name, desc, members)

# -------------------------------
# fetch_project_by_pid tests
# -------------------------------
def test_fetch_project_by_pid_found(mock_client, supabase_client):
    pid = 10
    expected = {"id": pid, "uid": "user123", "name": "Proj", "desc": "D", "department": "OPS"}
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [expected]
    result = supabase_client.fetch_project_by_pid(pid)
    assert result == expected

def test_fetch_project_by_pid_not_found(mock_client, supabase_client):
    pid = 99
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.fetch_project_by_pid(pid)
    assert result is None

def test_fetch_project_by_pid_failure_raises(mock_client, supabase_client):
    pid = 1
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        supabase_client.fetch_project_by_pid(pid)

# -------------------------------
# fetch_project_by_uid tests
# -------------------------------
def test_fetch_project_by_uid_found_list(mock_client, supabase_client):
    uid = "user123"
    expected = [
        {"id": 1, "uid": uid, "name": "P1", "desc": "D1", "department": "HR"},
        {"id": 2, "uid": uid, "name": "P2", "desc": "D2", "department": "ENG"},
    ]
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected
    result = supabase_client.fetch_project_by_uid(uid)
    assert isinstance(result, list)
    assert result == expected

def test_fetch_project_by_uid_not_found(mock_client, supabase_client):
    uid = "nouser"
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.fetch_project_by_uid(uid)
    assert result is None

def test_fetch_project_by_uid_failure_raises(mock_client, supabase_client):
    uid = "user123"
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        supabase_client.fetch_project_by_uid(uid)

# -------------------------------
# delete_project tests
# -------------------------------
def test_delete_project_success(mock_client, supabase_client):
    pid = 10
    expected = {"id": pid}
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [expected]
    result = supabase_client.delete_project(pid)
    assert result == expected

def test_delete_project_not_found(mock_client, supabase_client):
    pid = 22
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.delete_project(pid)
    assert result is None

def test_delete_project_failure_raises(mock_client, supabase_client):
    pid = 22
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.side_effect = Exception("Delete failed")
    with pytest.raises(Exception):
        supabase_client.delete_project(pid)

# -------------------------------
# update_project tests
# -------------------------------
def test_update_project_success(mock_client, supabase_client):
    pid = 5
    updated = {"name": "New Name", "desc": "New Desc", "department": "FIN"}
    expected = {"id": pid, "uid": "user123", **updated}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [expected]
    result = supabase_client.update_project(pid, updated)
    assert result == expected

def test_update_project_not_found(mock_client, supabase_client):
    pid = 5
    updated = {"name": "New Name"}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.update_project(pid, updated)
    assert result is None

def test_update_project_failure_raises(mock_client, supabase_client):
    pid = 5
    updated = {"name": "New Name"}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.side_effect = Exception("Update failed")
    with pytest.raises(Exception, match="Update failed"):
        supabase_client.update_project(pid, updated)

# -------------------------------
# get_all_logs tests
# -------------------------------
def test_get_all_logs_success(mock_client, supabase_client):
    expected_logs = [
        {"id": "log1", "table_name": "PROJECT", "action": "INSERT", "record_id": "project123"},
        {"id": "log2", "table_name": "PROJECT", "action": "UPDATE", "record_id": "project456"}
    ]
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected_logs
    result = supabase_client.get_all_logs()
    assert result == expected_logs

def test_get_all_logs_with_filter(mock_client, supabase_client):
    filter_by = "project123"
    expected_logs = [
        {"id": "log1", "table_name": "PROJECT", "action": "INSERT", "record_id": "project123"}
    ]
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected_logs
    result = supabase_client.get_all_logs(filter_by)
    assert result == expected_logs

def test_get_all_logs_empty(mock_client, supabase_client):
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.get_all_logs()
    assert result == []

def test_get_all_logs_none_data(mock_client, supabase_client):
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = None
    result = supabase_client.get_all_logs()
    assert result == []

# -------------------------------
# fetch_all_projects tests
# -------------------------------
def test_fetch_all_projects_success(mock_client, supabase_client):
    expected = [
        {"id": 1, "name": "P1", "department": "ENG"},
        {"id": 2, "name": "P2", "department": "HR"}
    ]
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = expected
    result = supabase_client.fetch_all_projects()
    assert result == expected

def test_fetch_all_projects_empty(mock_client, supabase_client):
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = []
    result = supabase_client.fetch_all_projects()
    assert result is None  # Changed from assert result == []

# -------------------------------
# fetch_projects_by_department tests
# -------------------------------
def test_fetch_projects_by_department_success(mock_client, supabase_client):
    dept = "ENG"
    expected = [
        {"id": 1, "name": "P1", "department": "ENG"},
        {"id": 2, "name": "P2", "department": "ENG"}
    ]
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected
    result = supabase_client.get_projects_by_department(dept)  # Changed method name
    assert result == expected

def test_fetch_projects_by_department_empty(mock_client, supabase_client):
    dept = "MARKETING"
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    result = supabase_client.get_projects_by_department(dept)  # Changed method name
    assert result is None  # Changed from assert result == []

# ======================================================================
#                         ProjectService tests
# ======================================================================

# --- Shim for absolute imports ---
import sys as _sys

# 1) Make 'models' importable
import backend.services.atomic.project.models as _models
_sys.modules.setdefault("models", _models)

# 2) Make 'services' importable
import backend.services.atomic.project.services as _services
_sys.modules.setdefault("services", _services)

# Import ProjectService after shimming
from backend.services.atomic.project.services.project_service import ProjectService

@pytest.fixture
def mock_supabase_for_service():
    with patch("backend.services.atomic.project.services.project_service.SupabaseClient") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def project_service(mock_supabase_for_service):
    return ProjectService()

def test_service_get_all_projects(project_service, mock_supabase_for_service):
    expected = [{"id": 1}, {"id": 2}]
    mock_supabase_for_service.fetch_all_projects.return_value = expected
    result = project_service.get_all_projects()
    assert result == expected
    mock_supabase_for_service.fetch_all_projects.assert_called_once()

def test_service_get_project_by_id(project_service, mock_supabase_for_service):
    pid = "proj-123"
    expected = {"id": pid, "name": "Test"}
    mock_supabase_for_service.fetch_project_by_pid.return_value = expected
    result = project_service.get_project_by_id(pid)
    assert result == expected
    mock_supabase_for_service.fetch_project_by_pid.assert_called_once_with(pid)

def test_service_get_projects_by_user_id(project_service, mock_supabase_for_service):
    uid = "user-123"
    expected = [{"id": 1, "uid": uid}]
    mock_supabase_for_service.fetch_project_by_uid.return_value = expected
    result = project_service.get_projects_by_user_id(uid)
    assert result == expected
    mock_supabase_for_service.fetch_project_by_uid.assert_called_once_with(uid)

def test_service_create_project(project_service, mock_supabase_for_service):
    uid = "u1"
    name = "New"
    desc = "D"
    members = ["u1"]
    expected = {"id": "p1", "uid": uid, "name": name, "desc": desc, "members": members}
    mock_supabase_for_service.insert_project.return_value = expected
    result = project_service.create_project(uid, name, desc, members)  # Changed from dict to individual params
    assert result == expected
    mock_supabase_for_service.insert_project.assert_called_once_with(uid, name, desc, members)

def test_service_update_project(project_service, mock_supabase_for_service):
    pid = "p1"
    data = {"name": "Updated"}
    expected = {"id": pid, "name": "Updated"}
    mock_supabase_for_service.update_project.return_value = expected
    result = project_service.update_project(pid, data)
    assert result == expected
    mock_supabase_for_service.update_project.assert_called_once_with(pid, data)

def test_service_delete_project(project_service, mock_supabase_for_service):
    pid = "p1"
    expected = {"id": pid}
    mock_supabase_for_service.delete_project.return_value = expected
    result = project_service.delete_project(pid)
    assert result == expected
    mock_supabase_for_service.delete_project.assert_called_once_with(pid)

def test_service_get_all_logs_no_filter(project_service, mock_supabase_for_service):
    expected = [{"id": "log1"}]
    mock_supabase_for_service.get_all_logs.return_value = expected
    result = project_service.get_all_logs()
    assert result == expected
    mock_supabase_for_service.get_all_logs.assert_called_once_with(None)

def test_service_get_all_logs_with_filter(project_service, mock_supabase_for_service):
    filter_by = "p1"
    expected = [{"id": "log1", "record_id": "p1"}]
    mock_supabase_for_service.get_all_logs.return_value = expected
    result = project_service.get_all_logs(filter_by)
    assert result == expected
    mock_supabase_for_service.get_all_logs.assert_called_once_with(filter_by)

def test_service_get_projects_by_department(project_service, mock_supabase_for_service):
    dept = "ENG"
    # The mock data MUST include "owner_department" key because the service transforms it
    mock_response = [{"id": 1, "owner_department": "ENG"}]
    expected = [{"id": 1, "department": "ENG"}]  # Only department, NOT owner_department
    
    mock_supabase_for_service.get_projects_by_department.return_value = mock_response
    
    result = project_service.get_projects_by_department(dept)
    
    assert result == expected
    mock_supabase_for_service.get_projects_by_department.assert_called_once_with(dept)

# ======================================================================
#                         FastAPI main.py endpoint tests
# ======================================================================

# 3) Now import controllers and expose it as 'controllers'
import backend.services.atomic.project.controllers as _controllers
_sys.modules.setdefault("controllers", _controllers)

# 4) Finally import the FastAPI app
import backend.services.atomic.project.main as project_main

@pytest.fixture
def api_client(monkeypatch):
    fake = MagicMock()
    fake.get_all_projects.return_value = [{"id": "p1"}]
    fake.get_all_projects_by_dept.return_value = [{"id": "p2", "department": "ENG"}]
    fake.get_project_by_id.return_value = {"id": "p3"}
    fake.get_projects_by_user_id.return_value = [{"id": "p4", "uid": "u1"}]
    fake.create_project.return_value = {"id": "p5"}
    fake.update_project.return_value = {"id": "p6"}
    fake.delete_project.return_value = {"id": "p7"}
    fake.get_all_logs.return_value = [{"id": "l1"}]
    fake.get_projects_by_department.return_value = [{"id": "p8", "department": "HR"}]

    monkeypatch.setattr(project_main, "project_controller", fake)
    return TestClient(project_main.app), fake

def test_root_and_favicon(api_client):
    client, _ = api_client
    assert client.get("/").status_code == 200
    assert client.get("/favicon.ico").status_code == 204

def test_get_all_projects(api_client):
    client, ctrl = api_client
    assert client.get("/all").status_code == 200
    ctrl.get_all_projects.assert_called_once()

def test_get_all_projects_by_dept(api_client):
    client, ctrl = api_client
    assert client.get("/dept/ENG").status_code == 200
    ctrl.get_all_projects_by_dept.assert_called_once_with("ENG")

def test_get_project_by_id(api_client):
    client, ctrl = api_client
    assert client.get("/pid/XYZ").status_code == 200
    ctrl.get_project_by_id.assert_called_once_with("XYZ")

def test_get_projects_by_user_id(api_client):
    client, ctrl = api_client
    assert client.get("/uid/USER1").status_code == 200
    ctrl.get_projects_by_user_id.assert_called_once_with("USER1")

def test_insert_new_project(api_client):
    client, ctrl = api_client
    payload = {"uid": "u1", "name": "Proj", "desc": "D", "department": "FIN"}
    r = client.post("/", json=payload)
    assert r.status_code == 200
    ctrl.create_project.assert_called_once_with(payload)

def test_update_project(api_client):
    client, ctrl = api_client
    payload = {"name": "New", "department": "OPS"}
    assert client.put("/P123", json=payload).status_code == 200
    ctrl.update_project.assert_called_once_with("P123", payload)

def test_delete_project(api_client):
    client, ctrl = api_client
    assert client.delete("/DELX").status_code == 200
    ctrl.delete_project.assert_called_once_with("DELX")

def test_get_all_logs(api_client):
    client, ctrl = api_client
    assert client.get("/logs").status_code == 200
    ctrl.get_all_logs.assert_called_once()

def test_get_log_found(api_client):
    client, ctrl = api_client
    ctrl.get_all_logs.return_value = [{"id": "log-abc"}]
    assert client.get("/logs/log-abc").status_code == 200
    ctrl.get_all_logs.assert_called_with(filter_by="log-abc")

def test_get_log_not_found_returns_404(monkeypatch):
    import backend.services.atomic.project.main as project_main
    fake = MagicMock()
    fake.get_all_logs.return_value = []
    monkeypatch.setattr(project_main, "project_controller", fake)
    client = _TC(project_main.app, raise_server_exceptions=False)
    assert client.get("/logs/does-not-exist").status_code == 404

def test_get_projects_by_department(api_client):
    client, ctrl = api_client
    assert client.get("/department/HR").status_code == 200
    ctrl.get_projects_by_department.assert_called_once_with("HR")

# ======================================================================
#                    ProjectController tests
# ======================================================================

@pytest.fixture
def mock_service_for_controller():
    with patch("backend.services.atomic.project.controllers.project_controller.ProjectService") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def project_controller(mock_service_for_controller):
    from backend.services.atomic.project.controllers.project_controller import ProjectController
    return ProjectController()

# Test get_all_projects
def test_controller_get_all_projects_success(project_controller, mock_service_for_controller):
    mock_data = [
        {"id": "1", "uid": "u1", "name": "P1", "desc": "D1", "members": ["u1"], "department": "ENG"},
        {"id": "2", "uid": "u2", "name": "P2", "desc": "D2", "members": [], "department": "HR"}
    ]
    mock_service_for_controller.get_all_projects.return_value = mock_data
    result = project_controller.get_all_projects()
    assert result.message == "2 project(s) retrieved"
    assert len(result.project) == 2

def test_controller_get_all_projects_empty(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_all_projects.return_value = []
    result = project_controller.get_all_projects()
    assert result.message == "No projects found"
    assert result.project == []

def test_controller_get_all_projects_with_none_members(project_controller, mock_service_for_controller):
    mock_data = [{"id": "1", "uid": "u1", "name": "P1", "desc": "D1", "members": None, "department": "ENG"}]
    mock_service_for_controller.get_all_projects.return_value = mock_data
    result = project_controller.get_all_projects()
    assert result.project[0].members == []

def test_controller_get_all_projects_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_all_projects.side_effect = Exception("DB Error")
    with pytest.raises(HTTPException) as exc:
        project_controller.get_all_projects()
    assert exc.value.status_code == 500

# Test get_all_projects_by_dept
def test_controller_get_all_projects_by_dept_success(project_controller, mock_service_for_controller):
    dept = "ENG"
    mock_data = [{"id": "1", "uid": "u1", "name": "P1", "desc": "D1", "members": ["u1"], "department": "ENG"}]
    mock_service_for_controller.get_all_projects_by_dept.return_value = mock_data
    result = project_controller.get_all_projects_by_dept(dept)
    assert "1 project(s) retrieved for department 'ENG'" in result.message
    assert len(result.project) == 1

def test_controller_get_all_projects_by_dept_empty(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_all_projects_by_dept.return_value = []
    result = project_controller.get_all_projects_by_dept("MARKETING")
    assert "No projects found for department 'MARKETING'" in result.message

def test_controller_get_all_projects_by_dept_with_extra_fields(project_controller, mock_service_for_controller):
    # Test that extra fields like owner_department are filtered out
    mock_data = [{"id": "1", "uid": "u1", "name": "P1", "desc": "D1", "members": ["u1"], 
                  "department": "ENG", "owner_department": "ENG"}]
    mock_service_for_controller.get_all_projects_by_dept.return_value = mock_data
    result = project_controller.get_all_projects_by_dept("ENG")
    assert len(result.project) == 1

def test_controller_get_all_projects_by_dept_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_all_projects_by_dept.side_effect = Exception("DB Error")
    with pytest.raises(HTTPException) as exc:
        project_controller.get_all_projects_by_dept("ENG")
    assert exc.value.status_code == 500

# Test get_project_by_id
def test_controller_get_project_by_id_found(project_controller, mock_service_for_controller):
    pid = "p1"
    mock_data = {"id": pid, "uid": "u1", "name": "P1", "desc": "D1", "members": ["u1"], "department": "ENG"}
    mock_service_for_controller.get_project_by_id.return_value = mock_data
    result = project_controller.get_project_by_id(pid)
    assert f"Project with Project ID {pid} retrieved successfully" in result.message
    assert result.project.id == pid

def test_controller_get_project_by_id_not_found(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_project_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        project_controller.get_project_by_id("nonexistent")
    assert exc.value.status_code == 404

def test_controller_get_project_by_id_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_project_by_id.side_effect = Exception("DB Error")
    with pytest.raises(HTTPException) as exc:
        project_controller.get_project_by_id("p1")
    assert exc.value.status_code == 500

# Test get_projects_by_user_id
def test_controller_get_projects_by_user_id_found(project_controller, mock_service_for_controller):
    uid = "u1"
    mock_data = [{"id": "p1", "uid": uid, "name": "P1", "desc": "D1", "members": [uid], "department": "ENG"}]
    mock_service_for_controller.get_projects_by_user_id.return_value = mock_data
    result = project_controller.get_projects_by_user_id(uid)
    assert f"Projects with user id {uid} retrieved successfully" in result.message
    assert len(result.project) == 1

def test_controller_get_projects_by_user_id_not_found(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_projects_by_user_id.return_value = []
    with pytest.raises(HTTPException) as exc:
        project_controller.get_projects_by_user_id("u999")
    assert exc.value.status_code == 404

def test_controller_get_projects_by_user_id_none(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_projects_by_user_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        project_controller.get_projects_by_user_id("u999")
    assert exc.value.status_code == 404

def test_controller_get_projects_by_user_id_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.get_projects_by_user_id.side_effect = Exception("DB Error")
    with pytest.raises(HTTPException) as exc:
        project_controller.get_projects_by_user_id("u1")
    assert exc.value.status_code == 500

# Test create_project
def test_controller_create_project_success(project_controller, mock_service_for_controller):
    project_data = {"uid": "u1", "name": "New Project", "desc": "Description", "members": ["u1"]}
    mock_created = {"id": "p1", **project_data, "department": "ENG"}
    mock_service_for_controller.create_project.return_value = mock_created
    result = project_controller.create_project(project_data)
    assert "Project Inserted Successfully" in result.message
    assert result.project.name == "New Project"

def test_controller_create_project_missing_uid(project_controller, mock_service_for_controller):
    project_data = {"name": "New Project"}
    with pytest.raises(HTTPException) as exc:
        project_controller.create_project(project_data)
    assert exc.value.status_code == 400
    assert "uid is required" in str(exc.value.detail)

def test_controller_create_project_missing_name(project_controller, mock_service_for_controller):
    project_data = {"uid": "u1"}
    with pytest.raises(HTTPException) as exc:
        project_controller.create_project(project_data)
    assert exc.value.status_code == 400
    assert "name is required" in str(exc.value.detail)

def test_controller_create_project_failed(project_controller, mock_service_for_controller):
    project_data = {"uid": "u1", "name": "New Project"}
    mock_service_for_controller.create_project.return_value = None
    with pytest.raises(HTTPException) as exc:
        project_controller.create_project(project_data)
    assert exc.value.status_code == 500

def test_controller_create_project_error(project_controller, mock_service_for_controller):
    project_data = {"uid": "u1", "name": "New Project"}
    mock_service_for_controller.create_project.side_effect = Exception("Creation error")
    with pytest.raises(HTTPException) as exc:
        project_controller.create_project(project_data)
    assert exc.value.status_code == 400

# Test update_project
def test_controller_update_project_success(project_controller, mock_service_for_controller):
    pid = "p1"
    update_data = {"name": "Updated Name"}
    mock_updated = {"id": pid, "uid": "u1", "name": "Updated Name", "desc": "D", "members": [], "department": "ENG"}
    mock_service_for_controller.update_project.return_value = mock_updated
    result = project_controller.update_project(pid, update_data)
    assert f"Project {pid} Project Updated Successfully" in result.message

def test_controller_update_project_empty_payload(project_controller, mock_service_for_controller):
    with pytest.raises(HTTPException) as exc:
        project_controller.update_project("p1", {})
    assert exc.value.status_code == 400
    assert "Update payload cannot be empty" in str(exc.value.detail)

def test_controller_update_project_not_found(project_controller, mock_service_for_controller):
    mock_service_for_controller.update_project.return_value = None
    with pytest.raises(HTTPException) as exc:
        project_controller.update_project("p999", {"name": "New"})
    assert exc.value.status_code == 404

def test_controller_update_project_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.update_project.side_effect = Exception("Update error")
    with pytest.raises(HTTPException) as exc:
        project_controller.update_project("p1", {"name": "New"})
    assert exc.value.status_code == 400

# Test delete_project
def test_controller_delete_project_success(project_controller, mock_service_for_controller):
    pid = "p1"
    mock_service_for_controller.delete_project.return_value = {"id": pid}
    result = project_controller.delete_project(pid)
    assert f"Project {pid} deleted successfully" in result["message"]

def test_controller_delete_project_not_found(project_controller, mock_service_for_controller):
    mock_service_for_controller.delete_project.return_value = None
    with pytest.raises(HTTPException) as exc:
        project_controller.delete_project("p999")
    assert exc.value.status_code == 404

def test_controller_delete_project_error(project_controller, mock_service_for_controller):
    mock_service_for_controller.delete_project.side_effect = Exception("Delete error")
    with pytest.raises(HTTPException) as exc:
        project_controller.delete_project("p1")
    assert exc.value.status_code == 500

# Test get_all_logs
def test_controller_get_all_logs(project_controller, mock_service_for_controller):
    mock_logs = [{"id": "log1", "action": "INSERT"}]
    mock_service_for_controller.get_all_logs.return_value = mock_logs
    result = project_controller.get_all_logs()
    assert result == mock_logs

def test_controller_get_all_logs_with_filter(project_controller, mock_service_for_controller):
    mock_logs = [{"id": "log1", "record_id": "p1"}]
    mock_service_for_controller.get_all_logs.return_value = mock_logs
    result = project_controller.get_all_logs("p1")
    assert result == mock_logs

# Test get_projects_by_department
def test_controller_get_projects_by_department(project_controller, mock_service_for_controller):
    from backend.services.atomic.project.models.project import ProjectListResponse
    mock_response = ProjectListResponse(message="Success", project=[])
    mock_service_for_controller.get_projects_by_department.return_value = mock_response
    result = project_controller.get_projects_by_department("ENG")
    assert result == mock_response

# ======================================================================
#                    Additional Service Coverage
# ======================================================================

def test_service_get_all_projects_by_dept(project_service, mock_supabase_for_service):
    dept = "ENG"
    expected = [{"id": 1, "owner_department": "ENG"}]
    mock_supabase_for_service.get_projects_by_department.return_value = expected
    result = project_service.get_all_projects_by_dept(dept)
    assert result == expected
    mock_supabase_for_service.get_projects_by_department.assert_called_once_with(dept)

def test_service_get_all_projects_by_dept_none(project_service, mock_supabase_for_service):
    mock_supabase_for_service.get_projects_by_department.return_value = None
    result = project_service.get_all_projects_by_dept("MARKETING")
    assert result == []