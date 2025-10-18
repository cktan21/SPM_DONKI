import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.atomic.schedule.supabaseClient import SupabaseClient


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def mock_client():
    """Patch create_client and return a mocked Supabase client."""
    with patch("backend.services.atomic.schedule.supabaseClient.create_client") as mock_create_client:
        client = MagicMock()
        mock_create_client.return_value = client
        yield client


@pytest.fixture
def supabase_client(mock_client):
    """Return SupabaseClient with mocked client."""
    return SupabaseClient()


# -------------------------------
# Insert tests
# -------------------------------
def test_insert_schedule_success(mock_client, supabase_client):
    tid = "1991067d-18d4-48c4-987b-7c067..."
    deadline = "2025-09-26T15:42:21+00:00"
    status = "ongoing"

    # fetch_schedule should return None (no conflict)
    supabase_client.fetch_schedule = MagicMock(return_value=None)

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {"tid": tid, "deadline": deadline, "status": status}
    ]

    result = supabase_client.insert_schedule(tid, deadline, status)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.insert.assert_called_once_with({
        "tid": tid,
        "deadline": deadline,
        "status": status
    })
    assert result["tid"] == tid
    assert result["deadline"] == deadline
    assert result["status"] == status


# def test_insert_schedule_duplicate_tid(mock_client, supabase_client):
#     tid = "duplicate-task"
#     supabase_client.fetch_schedule = MagicMock(return_value={"tid": tid})

#     with pytest.raises(Exception) as excinfo:
#         supabase_client.insert_schedule(tid, "2025-10-11T03:58:20+00:00", "ongoing")
#     assert "Task with this ID already exists." in str(excinfo.value)


def test_insert_schedule_no_data_returned(mock_client, supabase_client):
    tid = "new-task"
    supabase_client.fetch_schedule = MagicMock(return_value=None)

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = []

    result = supabase_client.insert_schedule(tid, "2025-10-11T03:58:20+00:00", "ongoing")
    assert result is None


# -------------------------------
# Fetch tests
# -------------------------------
def test_fetch_schedule_found(mock_client, supabase_client):
    tid = "1991067d-18d4-48c4-987b-7c067..."
    expected = {"tid": tid, "status": "ongoing"}

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [expected]

    result = supabase_client.fetch_schedule(tid)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("tid", tid)
    assert result == expected


def test_fetch_schedule_not_found(mock_client, supabase_client):
    tid = "missing-task"

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.fetch_schedule(tid)
    assert result is None


# -------------------------------
# Update tests
# -------------------------------
def test_update_schedule_success(mock_client, supabase_client):
    tid = "update-task"
    updated_data = {"status": "overdue"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [
        {"tid": tid, "status": "overdue"}
    ]

    result = supabase_client.update_schedule(tid, updated_data)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.update.assert_called_once_with(updated_data)
    mock_table.update.return_value.eq.assert_called_once_with("tid", tid)
    assert result["status"] == "overdue"


def test_update_schedule_no_result(mock_client, supabase_client):
    tid = "ghost-task"
    updated_data = {"status": "overdue"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.update_schedule(tid, updated_data)
    assert result is None


# -------------------------------
# Delete tests
# -------------------------------
def test_delete_schedule_success(mock_client, supabase_client):
    tid = "delete-task"
    deleted = {"tid": tid, "status": "ongoing"}

    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [deleted]

    result = supabase_client.delete_schedule(tid)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.delete.return_value.eq.assert_called_once_with("tid", tid)
    assert result == deleted


def test_delete_schedule_not_found(mock_client, supabase_client):
    tid = "missing-task"

    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.delete_schedule(tid)
    assert result is None
