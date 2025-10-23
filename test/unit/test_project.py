import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.project.services.supabaseClient import SupabaseClient


# -------------------------------
# Fixtures
# -------------------------------
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
    """Test successful project creation"""
    uid = "user-123"
    name = "New Project"
    desc = "Project Description"
    expected = {"id": "project-1", "uid": uid, "name": name, "desc": desc}

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [expected]

    result = supabase_client.insert_project(uid, name, desc)

    mock_client.table.assert_called_once_with("PROJECT")
    mock_table.insert.assert_called_once_with({
        "uid": uid,
        "name": name,
        "desc": desc
    })
    assert result == expected


def test_insert_project_without_description(mock_client, supabase_client):
    """Test project creation without description"""
    uid = "user-123"
    name = "Simple Project"
    desc = None

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {"id": "project-1", "uid": uid, "name": name, "desc": None}
    ]

    result = supabase_client.insert_project(uid, name, desc)

    mock_table.insert.assert_called_once_with({
        "uid": uid,
        "name": name,
        "desc": desc
    })
    assert result["name"] == name
    assert result["desc"] is None


def test_insert_project_empty_result(mock_client, supabase_client):
    """Test project creation when no data is returned"""
    uid, name, desc = "user123", "My Project", "Description"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = []

    result = supabase_client.insert_project(uid, name, desc)

    assert result is None


def test_insert_project_failure_raises(mock_client, supabase_client):
    """Test project creation with database error"""
    uid, name, desc = "user123", "My Project", "Description"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.side_effect = Exception("Insert failed")

    with pytest.raises(Exception, match="Insert failed"):
        supabase_client.insert_project(uid, name, desc)


# -------------------------------
# fetch_project_by_pid tests
# -------------------------------
def test_fetch_project_by_pid_found(mock_client, supabase_client):
    pid = 10
    expected = {"id": pid, "uid": "user123", "name": "Proj", "desc": "D"}

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [expected]

    result = supabase_client.fetch_project_by_pid(pid)

    mock_client.table.assert_called_once_with("PROJECT")
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
        {"id": 1, "uid": uid, "name": "P1", "desc": "D1"},
        {"id": 2, "uid": uid, "name": "P2", "desc": "D2"},
    ]

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected

    result = supabase_client.fetch_project_by_uid(uid)

    mock_client.table.assert_called_once_with("PROJECT")
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

    mock_client.table.assert_called_once_with("PROJECT")
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
    updated = {"name": "New Name", "desc": "New Desc"}
    expected = {"id": pid, "uid": "user123", **updated}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [expected]

    result = supabase_client.update_project(pid, updated)

    mock_client.table.assert_called_once_with("PROJECT")
    mock_table.update.assert_called_once_with(updated)
    assert result == expected


def test_update_project_not_found(mock_client, supabase_client):
    pid = 5
    updated = {"name": "New Name"}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.update_project(pid, updated)

    assert result is None


def test_update_project_failure_raises(mock_client, supabase_client):
    """Test project update with database error"""
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
    """Test getting all audit logs for projects"""
    expected_logs = [
        {"id": "log1", "table_name": "PROJECT", "action": "INSERT", "record_id": "project123"},
        {"id": "log2", "table_name": "PROJECT", "action": "UPDATE", "record_id": "project456"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected_logs
    
    result = supabase_client.get_all_logs()
    
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("table_name", "PROJECT")
    assert result == expected_logs


def test_get_all_logs_with_filter(mock_client, supabase_client):
    """Test getting audit logs with filter"""
    filter_by = "project123"
    expected_logs = [
        {"id": "log1", "table_name": "PROJECT", "action": "INSERT", "record_id": "project123"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected_logs
    
    result = supabase_client.get_all_logs(filter_by)
    
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_table.select.assert_called_once_with("*")
    assert result == expected_logs


def test_get_all_logs_empty(mock_client, supabase_client):
    """Test getting audit logs when no logs exist"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []
    
    result = supabase_client.get_all_logs()
    
    assert result == []


def test_get_all_logs_none_data(mock_client, supabase_client):
    """Test getting audit logs when data is None"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_logs()
    
    assert result == []
