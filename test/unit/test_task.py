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

# To confirm that your sample_create_payload function: Builds a default task payload dictionary correctly. Properly applies any overrides you pass in (since it uses payload.update(overrides)).
def test_sample_create_payload_overrides_are_applied():
    # Baseline call executes helper body
    base = sample_create_payload()
    assert base["name"] == "New Task Title"
    # Override path executes payload.update(overrides)
    out = sample_create_payload(name="X", created_by_uid="u-override")
    assert out["name"] == "X"
    assert out["created_by_uid"] == "u-override"
    # unchanged keys still present
    assert "desc" in out and "notes" in out

# confirm that your sample_update_payload function: Returns the expected default task update payload.Correctly merges overrides into the default dictionary.
def test_sample_update_payload_overrides_are_applied():
    # Baseline call executes helper body
    base = sample_update_payload()
    assert base["name"] == "Complete Project Setup"
    # Override path executes payload.update(overrides)
    over = sample_update_payload(
        name="Y",
        parentTaskId=None,
        collaborators=[],
        pid="proj-x",
        desc="d",
        notes="n",
    )
    assert over["name"] == "Y"
    assert over["parentTaskId"] is None
    assert over["collaborators"] == []
    assert over["pid"] == "proj-x"
    assert over["desc"] == "d"
    assert over["notes"] == "n"


# -------------------------------
# Get All Tasks tests
# -------------------------------
def test_get_all_tasks_success(mock_client, supabase_client):
    """Test successful retrieval of all tasks"""
    expected_tasks = [
        {"id": "task-1", "name": "Complete Project Setup", "status": "ongoing"},
        {"id": "task-2", "name": "Review Code", "status": "pending"}
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
    filter_by = {"created_by_uid": "user123", "status": "ongoing"}
    expected_tasks = [{"id": "task1", "created_by_uid": "user123", "status": "ongoing"}]
    
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected_tasks
    
    result = supabase_client.get_all_tasks(filter_by)
    
    # Verify the method was called and returned expected result
    mock_client.table.assert_called_once_with("TASK")
    mock_table.select.assert_called_once_with("*")
    assert result == expected_tasks


def test_get_all_tasks_none_data(mock_client, supabase_client):
    """Test get_all_tasks when data is None"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.return_value.data = None
    
    result = supabase_client.get_all_tasks()
    
    assert result == []


# -------------------------------
# Update Task tests
# -------------------------------
def test_update_task_success(mock_client, supabase_client):
    """Test successful task update"""
    task_id = "task-123"
    updates = {"name": "Updated Task Name", "status": "completed"}
    updated_task = {"id": task_id, "name": "Updated Task Name", "status": "completed"}
    
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


def test_update_task_partial_update(mock_client, supabase_client):
    """Test updating task with partial data"""
    task_id = "task-123"
    updates = {"status": "overdue"}  # Only update status
    updated_task = {"id": task_id, "name": "Original Name", "status": "overdue"}
    
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated_task]
    
    result = supabase_client.update_task(task_id, updates)
    
    mock_table.update.assert_called_once_with(updates)
    assert result.data == [updated_task]


# -------------------------------
# Delete Task tests
# -------------------------------
def test_delete_task_success(mock_client, supabase_client):
    """Test successful task deletion"""
    task_id = "task-123"
    deleted_task = {"id": task_id, "name": "Deleted Task", "status": "completed"}
    
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


# -------------------------------
# Audit Logs tests
# -------------------------------
def test_get_all_logs_success(mock_client, supabase_client):
    """Test getting all audit logs for tasks"""
    expected_logs = [
        {"id": "log1", "table_name": "TASK", "action": "INSERT", "record_id": "task123"},
        {"id": "log2", "table_name": "SCHEDULE", "action": "UPDATE", "record_id": "schedule456"}
    ]
    
    # Mock the entire chain - task service uses .in_() for table_name
    mock_response = MagicMock()
    mock_response.data = expected_logs
    mock_client.table.return_value.select.return_value.in_.return_value.execute.return_value = mock_response
    
    result = supabase_client.get_all_logs()
    
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_client.table.return_value.select.assert_called_once_with("*")
    mock_client.table.return_value.select.return_value.in_.assert_called_once_with('table_name', ['TASK', 'SCHEDULE'])
    assert result == expected_logs


def test_get_all_logs_with_filter(mock_client, supabase_client):
    """Test getting audit logs with filter"""
    filter_by = "task123"
    expected_logs = [
        {"id": "log1", "table_name": "TASK", "action": "INSERT", "record_id": "task123"}
    ]
    
    # Mock the entire chain - task service uses .in_() then .eq()
    mock_response = MagicMock()
    mock_response.data = expected_logs
    mock_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = mock_response
    
    result = supabase_client.get_all_logs(filter_by)
    
    mock_client.table.assert_called_once_with("AUDIT_TRAIL")
    mock_client.table.return_value.select.assert_called_once_with("*")
    mock_client.table.return_value.select.return_value.in_.assert_called_once_with('table_name', ['TASK', 'SCHEDULE'])
    mock_client.table.return_value.select.return_value.in_.return_value.eq.assert_called_once_with("record_id", filter_by)
    assert result == expected_logs


def test_get_all_logs_empty(mock_client, supabase_client):
    """Test getting audit logs when no logs exist"""
    # Mock the entire chain
    mock_response = MagicMock()
    mock_response.data = []
    mock_client.table.return_value.select.return_value.in_.return_value.execute.return_value = mock_response
    
    result = supabase_client.get_all_logs()
    
    assert result == []


# -------------------------------
# Error Handling tests
# -------------------------------
def test_get_all_tasks_database_error(mock_client, supabase_client):
    """Test get_all_tasks with database error"""
    mock_table = mock_client.table.return_value
    mock_table.select.return_value.execute.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        supabase_client.get_all_tasks()


def test_update_task_database_error(mock_client, supabase_client):
    """Test update task with database error"""
    task_id = "task-123"
    updates = {"name": "Updated Task"}
    
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        supabase_client.update_task(task_id, updates)


def test_delete_task_database_error(mock_client, supabase_client):
    """Test delete task with database error"""
    task_id = "task-123"
    
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.side_effect = Exception("Database error")
    
    with pytest.raises(Exception, match="Database error"):
        supabase_client.delete_task(task_id)


# -------------------------------
# Additional coverage for new columns & paths
# -------------------------------

def test_get_all_tasks_filter_by_pid_and_parent(mock_client, supabase_client):
    """Cover filters for pid and parentTaskId (newer columns used by routes)."""
    expected = [
        {"id": "t1", "pid": "p-1", "parentTaskId": "pt-9", "status": "ongoing"},
    ]
    mock_table = mock_client.table.return_value
    # Chain: select().eq("pid", ...).eq("parentTaskId", ...).execute().data
    mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected

    result = supabase_client.get_all_tasks({"pid": "p-1", "parentTaskId": "pt-9"})

    mock_client.table.assert_called_once_with("TASK")
    mock_table.select.assert_called_once_with("*")
    assert result == expected


def test_get_all_tasks_filter_by_created_by_and_status_and_pid(mock_client, supabase_client):
    """Cover multi-key filter including created_by_uid + status + pid."""
    expected = [
        {"id": "t9", "created_by_uid": "u-1", "status": "incomplete", "pid": "proj-77"},
    ]
    mock_table = mock_client.table.return_value
    # Chain three eq() calls
    mock_table.select.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected

    result = supabase_client.get_all_tasks(
        {"created_by_uid": "u-1", "status": "incomplete", "pid": "proj-77"}
    )
    assert result == expected


def test_update_task_with_priority_label_and_collaborators(mock_client, supabase_client):
    """Ensure complex update payload (new columns) is passed through intact."""
    task_id = "task-new"
    updates = {
        "name": "Kickoff",
        "desc": "Initial setup",
        "notes": "Check README",
        "priorityLevel": 10,     # new column in usage
        "label": "Setup",        # new column in usage
        "collaborators": [       # existing but not previously covered
            "3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001",
            "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002",
        ],
        "pid": "proj-abc",       # ensure project linkage updates fine
        "parentTaskId": None,    # explicitly set None
    }
    updated = {**updates, "id": task_id}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

    resp = supabase_client.update_task(task_id, updates)

    mock_client.table.assert_called_once_with("TASK")
    mock_table.update.assert_called_once_with(updates)
    mock_table.update.return_value.eq.assert_called_once_with("id", task_id)
    assert resp.data == [updated]


def test_update_task_only_label(mock_client, supabase_client):
    """Minimal update touching just 'label' column."""
    task_id = "task-222"
    updates = {"label": "Blocked"}
    updated = {"id": task_id, "label": "Blocked"}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

    resp = supabase_client.update_task(task_id, updates)
    assert resp.data == [updated]


def test_update_task_only_priority(mock_client, supabase_client):
    """Minimal update touching just 'priorityLevel' column."""
    task_id = "task-333"
    updates = {"priorityLevel": 2}
    updated = {"id": task_id, "priorityLevel": 2}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

    resp = supabase_client.update_task(task_id, updates)
    assert resp.data == [updated]


def test_delete_task_accepts_string_ids(mock_client, supabase_client):
    """Ensure delete path is agnostic to UUID vs other string IDs."""
    task_id = "custom-string-id"
    deleted = {"id": task_id}
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [deleted]

    resp = supabase_client.delete_task(task_id)
    mock_client.table.assert_called_once_with("TASK")
    assert resp.data == [deleted]


def test_get_all_logs_filter_schedule_record(mock_client, supabase_client):
    """Cover log filtering when table_name includes SCHEDULE and record_id is given."""
    expected_logs = [
        {"id": "l-1", "table_name": "SCHEDULE", "action": "UPDATE", "record_id": "sched-42"},
    ]
    mock_response = MagicMock()
    mock_response.data = expected_logs
    # Chain: select().in_("table_name", ["TASK", "SCHEDULE"]).eq("record_id", tid).execute()
    mock_client.table.return_value.select.return_value.in_.return_value.eq.return_value.execute.return_value = (
        mock_response
    )

    out = supabase_client.get_all_logs("sched-42")
    assert out == expected_logs

# -------------------------------
# Edge Case tests
# -------------------------------

def test_get_all_tasks_filter_with_unknown_key(mock_client, supabase_client):
    """Unknown filter keys should still be passed through as .eq() calls."""
    expected = [{"id": "t1", "weird": "value"}]
    mock_table = mock_client.table.return_value
    # select().eq("weird","value").execute().data
    mock_table.select.return_value.eq.return_value.execute.return_value.data = expected

    out = supabase_client.get_all_tasks({"weird": "value"})
    mock_client.table.assert_called_once_with("TASK")
    mock_table.select.assert_called_once_with("*")
    assert out == expected


def test_get_all_tasks_filter_value_none(mock_client, supabase_client):
    """None values should flow through; DB may treat eq(None) specially."""
    mock_table = mock_client.table.return_value
    # select().eq("parentTaskId", None).execute().data
    mock_table.select.return_value.eq.return_value.execute.return_value.data = []

    out = supabase_client.get_all_tasks({"parentTaskId": None})
    assert out == []


def test_get_all_tasks_empty_filter_dict(mock_client, supabase_client):
    """Empty filter dict should behave like no filter (just select *)."""
    expected = [{"id": "t1"}, {"id": "t2"}]
    mock_table = mock_client.table.return_value
    # When no eq() is applied, service should just select().execute()
    mock_table.select.return_value.execute.return_value.data = expected

    out = supabase_client.get_all_tasks({})
    mock_client.table.assert_called_once_with("TASK")
    mock_table.select.assert_called_once_with("*")
    assert out == expected


def test_get_all_tasks_filter_mixed_types(mock_client, supabase_client):
    """Mixed data types in filters (int/bool/str) should pass through .eq() chain."""
    expected = [{"id": "t9", "priorityLevel": 10, "archived": False, "status": "incomplete"}]
    mock_table = mock_client.table.return_value
    # select().eq("priorityLevel",10).eq("archived",False).eq("status","incomplete").execute().data
    mock_table.select.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value.data = expected

    out = supabase_client.get_all_tasks({"priorityLevel": 10, "archived": False, "status": "incomplete"})
    assert out == expected


def test_update_task_empty_updates(mock_client, supabase_client):
    """Empty updates dict still results in an update call; DB may echo the row."""
    task_id = "task-empty"
    updated = {"id": task_id}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

    resp = supabase_client.update_task(task_id, {})
    mock_client.table.assert_called_once_with("TASK")
    mock_table.update.assert_called_once_with({})
    assert resp.data == [updated]


def test_update_task_none_data_then_fetches(mock_client, supabase_client):
    """If update returns data=None, service should fall back to a select fetch."""
    task_id = "t-x"
    mock_table = mock_client.table.return_value

    # update -> data=None
    mock_table.update.return_value.eq.return_value.execute.return_value.data = None
    # fallback select -> one row
    fetched = [{"id": task_id, "name": "After"}]
    mock_table.select.return_value.eq.return_value.execute.return_value.data = fetched

    resp = supabase_client.update_task(task_id, {"name": "X"})
    # both update & select get called
    mock_table.update.assert_called_once()
    mock_table.select.assert_called_once_with("*")
    assert resp.data == fetched


def test_update_task_set_collaborators_empty_list(mock_client, supabase_client):
    """Setting collaborators to an empty list should pass through correctly."""
    task_id = "t-collab"
    updates = {"collaborators": []}
    updated = {"id": task_id, "collaborators": []}
    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

    resp = supabase_client.update_task(task_id, updates)
    mock_table.update.assert_called_once_with(updates)
    assert resp.data == [updated]


def test_update_task_priority_boundaries(mock_client, supabase_client):
    """Boundary values for priorityLevel should be accepted as-is by the client layer."""
    task_id = "t-prio"
    for val in (1, 10):
        mock_table = mock_client.table.return_value
        updates = {"priorityLevel": val}
        updated = {"id": task_id, "priorityLevel": val}
        mock_table.update.return_value.eq.return_value.execute.return_value.data = [updated]

        resp = supabase_client.update_task(task_id, updates)
        assert resp.data == [updated]


def test_delete_task_special_char_id(mock_client, supabase_client):
    """IDs containing special characters should pass through untouched to .eq()."""
    task_id = "we!rd/id:123"
    deleted = {"id": task_id}
    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.return_value.data = [deleted]

    resp = supabase_client.delete_task(task_id)
    mock_client.table.assert_called_once_with("TASK")
    mock_table.delete.return_value.eq.assert_called_once_with("id", task_id)
    assert resp.data == [deleted]


def test_get_all_logs_none_data(mock_client, supabase_client):
    """Logs returning data=None should be normalized to []."""
    mock_resp = MagicMock()
    mock_resp.data = None
    mock_client.table.return_value.select.return_value.in_.return_value.execute.return_value = mock_resp

    out = supabase_client.get_all_logs()
    assert out == []