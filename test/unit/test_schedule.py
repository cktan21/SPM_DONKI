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
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = False
    status = "ongoing"
    next_occurrence = None

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {
            "tid": tid, 
            "start": start,
            "deadline": deadline, 
            "status": status,
            "is_recurring": is_recurring,
            "next_occurrence": next_occurrence
        }
    ]

    result = supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.insert.assert_called_once_with({
        "tid": tid,
        "start": start,
        "deadline": deadline,
        "status": status,
        "is_recurring": is_recurring,
        "next_occurrence": next_occurrence
    })
    assert result["tid"] == tid
    assert result["deadline"] == deadline
    assert result["status"] == status
    assert result["is_recurring"] == is_recurring


def test_insert_schedule_recurring_success(mock_client, supabase_client):
    tid = "recurring-task"
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = True
    status = "ongoing"
    next_occurrence = "2025-09-27T15:42:21+00:00"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {
            "tid": tid, 
            "start": start,
            "deadline": deadline, 
            "status": status,
            "is_recurring": is_recurring,
            "next_occurrence": next_occurrence
        }
    ]

    result = supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.insert.assert_called_once_with({
        "tid": tid,
        "start": start,
        "deadline": deadline,
        "status": status,
        "is_recurring": is_recurring,
        "next_occurrence": next_occurrence
    })
    assert result["tid"] == tid
    assert result["is_recurring"] == is_recurring
    assert result["next_occurrence"] == next_occurrence


# def test_insert_schedule_duplicate_tid(mock_client, supabase_client):
#     tid = "duplicate-task"
#     supabase_client.fetch_schedule = MagicMock(return_value={"tid": tid})

#     with pytest.raises(Exception) as excinfo:
#         supabase_client.insert_schedule(tid, "2025-10-11T03:58:20+00:00", "ongoing")
#     assert "Task with this ID already exists." in str(excinfo.value)


def test_insert_schedule_no_data_returned(mock_client, supabase_client):
    tid = "new-task"
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = False
    status = "ongoing"
    next_occurrence = None

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = []

    result = supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)
    assert result is None


# -------------------------------
# Fetch tests
# -------------------------------
def test_fetch_schedule_by_tid_found(mock_client, supabase_client):
    tid = "1991067d-18d4-48c4-987b-7c067..."
    expected = [{"tid": tid, "status": "ongoing", "sid": "schedule-1"}]

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected

    result = supabase_client.fetch_schedule_by_tid(tid)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("tid", tid)
    assert result == expected


def test_fetch_schedule_by_tid_not_found(mock_client, supabase_client):
    tid = "missing-task"

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.fetch_schedule_by_tid(tid)
    assert result is None


def test_fetch_schedule_by_tid_latest_found(mock_client, supabase_client):
    tid = "1991067d-18d4-48c4-987b-7c067..."
    expected = {"tid": tid, "status": "ongoing", "sid": "schedule-1", "created_at": "2025-10-18T08:34:34.969657+00:00"}

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value.data = [expected]

    result = supabase_client.fetch_schedule_by_tid(tid, latest=True)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("tid", tid)
    mock_table.select.return_value.eq.return_value.order.assert_called_once_with("created_at", desc=True)
    mock_table.select.return_value.eq.return_value.order.return_value.limit.assert_called_once_with(1)
    assert result == expected


def test_fetch_schedule_by_tid_latest_not_found(mock_client, supabase_client):
    tid = "missing-task"

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value.data = []

    result = supabase_client.fetch_schedule_by_tid(tid, latest=True)
    assert result is None


def test_fetch_schedule_by_sid_found(mock_client, supabase_client):
    sid = "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    expected = {"sid": sid, "tid": "task-1", "status": "ongoing"}

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = [expected]

    result = supabase_client.fetch_schedule_by_sid(sid)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("sid", sid)
    assert result == expected


def test_fetch_schedule_by_sid_not_found(mock_client, supabase_client):
    sid = "missing-schedule"

    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.fetch_schedule_by_sid(sid)
    assert result is None


# -------------------------------
# Update tests
# -------------------------------
def test_update_schedule_success(mock_client, supabase_client):
    sid = "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    updated_data = {"status": "overdue"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [
        {"sid": sid, "status": "overdue"}
    ]

    result = supabase_client.update_schedule(sid, updated_data)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.update.assert_called_once_with(updated_data)
    mock_table.update.return_value.eq.assert_called_once_with("sid", sid)
    assert result["status"] == "overdue"


def test_update_schedule_recurring_validation(mock_client, supabase_client):
    sid = "recurring-schedule"
    updated_data = {"is_recurring": True}  # Missing next_occurrence

    with pytest.raises(ValueError) as excinfo:
        supabase_client.update_schedule(sid, updated_data)
    assert "next_occurrence is required when is_recurring is True" in str(excinfo.value)


def test_update_schedule_recurring_success(mock_client, supabase_client):
    sid = "recurring-schedule"
    updated_data = {"is_recurring": True, "next_occurrence": "2025-12-31T23:59:59+00:00"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [
        {"sid": sid, "is_recurring": True, "next_occurrence": "2025-12-31T23:59:59+00:00"}
    ]

    result = supabase_client.update_schedule(sid, updated_data)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.update.assert_called_once_with(updated_data)
    mock_table.update.return_value.eq.assert_called_once_with("sid", sid)
    assert result["is_recurring"] == True
    assert result["next_occurrence"] == "2025-12-31T23:59:59+00:00"


def test_update_schedule_no_result(mock_client, supabase_client):
    sid = "ghost-schedule"
    updated_data = {"status": "overdue"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.update_schedule(sid, updated_data)
    assert result is None


# -------------------------------
# Delete tests
# -------------------------------
def test_delete_schedule_success(mock_client, supabase_client):
    sid = "053a4e96-cefd-4a8e-9941-5b621ff8ca52"
    deleted = {"sid": sid, "tid": "task-1", "status": "ongoing"}

    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [deleted]

    result = supabase_client.delete_schedule(sid)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.delete.return_value.eq.assert_called_once_with("sid", sid)
    assert result == deleted


def test_delete_schedule_not_found(mock_client, supabase_client):
    sid = "missing-schedule"

    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = []

    result = supabase_client.delete_schedule(sid)
    assert result is None
