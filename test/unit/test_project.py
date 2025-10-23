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
    uid, name, desc = "user123", "My Project", "Description"
    expected = {"id": 1, "uid": uid, "name": name, "desc": desc}

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [expected]

    result = supabase_client.insert_project(uid, name, desc)

    mock_client.table.assert_called_once_with("PROJECT")
    mock_table.insert.assert_called_once()
    assert result == expected


def test_insert_project_empty_result(mock_client, supabase_client):
    uid, name, desc = "user123", "My Project", "Description"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = []

    result = supabase_client.insert_project(uid, name, desc)

    assert result is None


def test_insert_project_failure_raises(mock_client, supabase_client):
    uid, name, desc = "user123", "My Project", "Description"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.side_effect = Exception("Insert failed")

    with pytest.raises(Exception):
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
    pid = 5
    updated = {"name": "New Name"}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.side_effect = Exception("Update failed")

    with pytest.raises(Exception):
        supabase_client.update_project(pid, updated)
