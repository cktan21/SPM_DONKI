import sys
import os
import pytest
import types
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from starlette.testclient import TestClient as _TC

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
    frequency = "Weekly"

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [
        {
            "tid": tid, 
            "start": start,
            "deadline": deadline, 
            "status": status,
            "is_recurring": is_recurring,
            "next_occurrence": next_occurrence,
            "frequency": frequency
        }
    ]

    result = supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence, frequency)

    mock_client.table.assert_called_once_with("SCHEDULE")
    mock_table.insert.assert_called_once_with({
        "tid": tid,
        "start": start,
        "deadline": deadline,
        "status": status,
        "is_recurring": is_recurring,
        "next_occurrence": next_occurrence,
        "frequency": frequency
    })
    assert result["tid"] == tid
    assert result["is_recurring"] == is_recurring
    assert result["next_occurrence"] == next_occurrence
    assert result["frequency"] == frequency

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


def test_insert_schedule_recurring_missing_next_occurrence(mock_client, supabase_client):
    """Test that creating a recurring schedule without next_occurrence raises validation error."""
    tid = "recurring-task"
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = True
    status = "ongoing"
    next_occurrence = None  # Missing required field for recurring schedule

    with pytest.raises(ValueError) as excinfo:
        supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)
    assert "next_occurrence is required when is_recurring is True" in str(excinfo.value)


def test_insert_schedule_recurring_missing_frequency(mock_client, supabase_client):
    """Test that creating a recurring schedule without frequency raises validation error."""
    tid = "recurring-task"
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = True
    status = "ongoing"
    next_occurrence = "2025-09-27T15:42:21+00:00"
    frequency = None  # Missing required field for recurring schedule

    with pytest.raises(ValueError) as excinfo:
        supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence, frequency)
    assert "frequency is required when is_recurring is True" in str(excinfo.value)


def test_insert_schedule_without_start(mock_client, supabase_client):
    """Test inserting schedule without start date"""
    tid = "task-123"
    start = None  # No start date
    deadline = "2025-12-31"
    is_recurring = False
    status = "pending"
    next_occurrence = None
    frequency = None
    
    expected = {
        "sid": "schedule-1",
        "tid": tid,
        "deadline": deadline,
        "status": status,
        "is_recurring": is_recurring,
        "next_occurrence": next_occurrence
    }
    
    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.return_value.data = [expected]
    
    result = supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence, frequency)
    
    # Verify start is not in the insert call when it's None
    call_args = mock_table.insert.call_args[0][0]
    assert "start" not in call_args
    assert result == expected


def test_insert_schedule_exception_raises(mock_client, supabase_client):
    """Test that insert_schedule raises exceptions from database"""
    tid = "task-error"
    start = "2025-09-25T15:42:21+00:00"
    deadline = "2025-09-26T15:42:21+00:00"
    is_recurring = False
    status = "ongoing"
    next_occurrence = None

    mock_table = mock_client.table.return_value
    mock_table.insert.return_value.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        supabase_client.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)


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
    mock_table.select.return_value.eq.return_value.order.assert_called_once_with("start", desc=True)
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


def test_supabase_client_fetch_schedule_by_tid_exception_raises(mock_client, supabase_client):
    mock_client.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("boom")
    with pytest.raises(Exception):
        supabase_client.fetch_schedule_by_tid("X")


def test_fetch_schedule_by_sid_exception_raises(mock_client, supabase_client):
    """Test that fetch_schedule_by_sid raises exceptions from database"""
    mock_client.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        supabase_client.fetch_schedule_by_sid("SID")


def test_fetch_recurring_tasks_success(mock_client, supabase_client):
    """Test fetching recurring tasks"""
    expected = [
        {"sid": "s1", "tid": "t1", "is_recurring": True, "frequency": "daily"},
        {"sid": "s2", "tid": "t2", "is_recurring": True, "frequency": "weekly"}
    ]
    
    mock_table = mock_client.table.return_value
    mock_select = mock_table.select.return_value
    mock_eq = mock_select.eq.return_value
    mock_not = mock_eq.not_
    mock_not.is_.return_value.execute.return_value.data = expected
    
    result = supabase_client.fetch_recurring_tasks()
    assert result == expected


def test_fetch_recurring_tasks_empty(mock_client, supabase_client):
    """Test fetching recurring tasks when none exist"""
    mock_table = mock_client.table.return_value
    mock_select = mock_table.select.return_value
    mock_eq = mock_select.eq.return_value
    mock_not = mock_eq.not_
    mock_not.is_.return_value.execute.return_value.data = []
    
    result = supabase_client.fetch_recurring_tasks()
    assert result == []


def test_fetch_recurring_tasks_exception_raises(mock_client, supabase_client):
    """Test that fetch_recurring_tasks raises exceptions from database"""
    mock_table = mock_client.table.return_value
    mock_select = mock_table.select.return_value
    mock_eq = mock_select.eq.return_value
    mock_not = mock_eq.not_
    mock_not.is_.return_value.execute.side_effect = Exception("DB error")
    
    with pytest.raises(Exception):
        supabase_client.fetch_recurring_tasks()


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


def test_update_schedule_exception_raises(mock_client, supabase_client):
    """Test that update_schedule raises exceptions from database"""
    sid = "schedule-error"
    updated_data = {"status": "overdue"}

    mock_table = mock_client.table.return_value
    mock_table.update.return_value.eq.return_value.execute.side_effect = Exception("Update failed")

    with pytest.raises(Exception, match="Update failed"):
        supabase_client.update_schedule(sid, updated_data)


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


def test_delete_schedule_exception_raises(mock_client, supabase_client):
    """Test that delete_schedule raises exceptions from database"""
    sid = "schedule-error"

    mock_table = mock_client.table.return_value
    mock_table.delete.return_value.eq.return_value.execute.side_effect = Exception("Delete failed")

    with pytest.raises(Exception, match="Delete failed"):
        supabase_client.delete_schedule(sid)



# --- inject fake supabaseClient BEFORE importing main ---
fake_module = types.ModuleType("supabaseClient")
fake_module.SupabaseClient = object  # dummy placeholder
sys.modules["supabaseClient"] = fake_module

import backend.services.atomic.schedule.main as main

# -----------------------------
# Helpers for httpx async stubs
# -----------------------------
class _FakeResponse:
    def __init__(self, status_code: int):
        self.status_code = status_code


class _FakeAsyncClient:
    """
    A context manager that yields itself and returns canned responses in sequence.
    - codes: list[int | Exception], we either return that status_code or raise.
    - counter: tracks number of POST calls.
    """
    def __init__(self, codes):
        self._codes = list(codes)
        self.calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def post(self, *args, **kwargs):
        self.calls += 1
        if not self._codes:
            return _FakeResponse(200) # pragma: no cover
        nxt = self._codes.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return _FakeResponse(nxt)


# -----------------------------
# Fixtures / client
# -----------------------------
def _wire_supabase(mock=None):
    """Replace module-level supabase with a mock client."""
    main.supabase = mock or MagicMock()

client = TestClient(main.app)


# =============================
# NOTIFIER COVERAGE (25-58, 62-95)
# =============================

def test_notify_added_success_on_first_url(monkeypatch):
    """
    Exercise early success path (status_code==200) for notify_recurring_task_added.
    Covers: loop, early return, no sleep/backoff.
    """
    fake = _FakeAsyncClient([200])
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda: fake)

    # no real delay
    # monkeypatch.setattr(asyncio, "sleep", lambda *_args, **_kw: asyncio.sleep(0))

    asyncio.run(main.notify_recurring_task_added({"sid": "S1", "tid": "T1"})) # pragma: no cover
    # Should have attempted exactly one POST
    assert fake.calls == 1 


def test_notify_added_all_fail_then_log(monkeypatch):
    """
    Exercise: non-200 statuses across all attempts & URLs + exceptions; ensure it completes.
    Covers: warning logging branches, exception branch, exponential backoff awaits.
    """
    # 3 attempts * 3 URLs = up to 9 POSTs; we provide many failing codes and one exception.
    codes = [500, 503, 404, Exception("boom"), 500, 500, 400, 502, 503]
    fake = _FakeAsyncClient(codes)
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda: fake)

    # Avoid real waiting; count calls implicitly via fake.calls
    async def _fast_sleep(_):
        return None
    monkeypatch.setattr(asyncio, "sleep", lambda *_a, **_k: _fast_sleep(0))

    asyncio.run(main.notify_recurring_task_added({"sid": "S2", "tid": "T2"}))
    # We don't assert log content; just that we exercised many calls.
    assert fake.calls >= 3  # definitely attempted multiple URLs/attempts


def test_notify_updated_fail_then_success(monkeypatch):
    """
    Exercise: first URL/attempt fails, second attempt succeeds -> early return.
    """
    fake = _FakeAsyncClient([500, 200])
    monkeypatch.setattr(main.httpx, "AsyncClient", lambda: fake)

    # no real delay
    monkeypatch.setattr(asyncio, "sleep", lambda *_args, **_kw: asyncio.sleep(0))

    asyncio.run(main.notify_recurring_task_updated({"sid": "S3", "tid": "T3"}))
    assert fake.calls == 2


# ==========================================
# EXCEPTION PATHS / BRANCHES IN ENDPOINTS
# ==========================================

def test_put_update_schedule_reraises_http_exception_branch():
    """
    Force 404 from fetch_schedule_by_sid to hit the explicit HTTPException branch
    inside update_schedule (lines around 173-174).
    """
    _wire_supabase()
    main.supabase.fetch_schedule_by_sid.return_value = None
    r = client.put("/NO_SUCH_SID", json={"status": "x"})
    assert r.status_code == 404


def test_put_update_schedule_generic_exception_to_400(monkeypatch):
    """
    Force a generic Exception in update path to hit the generic except -> 400.
    """
    _wire_supabase()
    main.supabase.fetch_schedule_by_sid.return_value = {"sid": "S99", "tid": "T99"}
    main.supabase.update_schedule.side_effect = Exception("boom!")
    r = client.put("/S99", json={"status": "x"})
    assert r.status_code == 400
    assert r.json()["detail"] == "boom!"


def test_put_update_by_tid_generic_exception_to_400(monkeypatch):
    """
    For update_schedule_by_tid: make it find schedule + sid, then raise generic Exception on update
    to hit the generic except (lines ~276-280 minus pragma).
    """
    _wire_supabase()
    main.supabase.fetch_schedule_by_tid.return_value = {"sid": "SID_TZ", "tid": "TZ"}
    main.supabase.update_schedule.side_effect = Exception("update failed")
    r = client.put("/tid/TZ", json={"status": "zzz"})
    assert r.status_code == 400
    assert r.json()["detail"] == "update failed"


def test_post_insert_schedule_generic_exception_to_400():
    """
    Force supabase.insert_schedule to raise to cover the POST route's except -> 400.
    """
    _wire_supabase()
    main.supabase.insert_schedule.side_effect = Exception("insert failed")
    payload = {
        "tid": "TTX",
        "start": "2025-01-01T00:00:00+00:00",
        "deadline": "2025-01-02T00:00:00+00:00",
        "status": "ongoing",
        "is_recurring": False,
    }
    r = client.post("/", json=payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "insert failed"


def test_get_recurring_all_exception_to_400():
    """
    Cover the except path in /recurring/all (lines around 249).
    """
    _wire_supabase()
    main.supabase.fetch_recurring_tasks.side_effect = Exception("bad read")
    r = client.get("/recurring/all")
    assert r.status_code == 400
    assert r.json()["detail"] == "bad read"


def test_put_update_by_tid_missing_schedule_404():
    """
    Ensure the 404 path for missing schedule in update-by-tid is covered.
    """
    _wire_supabase()
    main.supabase.fetch_schedule_by_tid.return_value = None
    r = client.put("/tid/MISSING", json={"status": "x"})
    assert r.status_code == 404


def test_put_update_by_tid_missing_sid_404():
    """
    Ensure the 404 path when schedule exists but has no sid.
    """
    _wire_supabase()
    main.supabase.fetch_schedule_by_tid.return_value = {"tid": "T_ONLY"}
    r = client.put("/tid/T_ONLY", json={"status": "x"})
    assert r.status_code == 404

# ======================================================================================================
#                                    FastAPI main.py endpoint tests
# ======================================================================================================
import backend.services.atomic.schedule.supabaseClient as _sc
import sys as _sys
_sys.modules.setdefault("supabaseClient", _sc)

import backend.services.atomic.schedule.main as schedule_main

@pytest.fixture
def fake_notify_spies(monkeypatch):
    """Patch notify coroutines to async no-ops we can spy on."""
    calls = {"added": 0, "updated": 0}

    async def _added(payload):
        calls["added"] += 1

    async def _updated(payload):
        calls["updated"] += 1

    monkeypatch.setattr(schedule_main, "notify_recurring_task_added", _added, raising=True)
    monkeypatch.setattr(schedule_main, "notify_recurring_task_updated", _updated, raising=True)
    return calls

@pytest.fixture
def api_client(monkeypatch):
    """Patch the module-level supabase in main.py and return a TestClient."""
    fake = MagicMock()
    monkeypatch.setattr(schedule_main, "supabase", fake, raising=True)
    return TestClient(schedule_main.app), fake  # (client, supabase_mock)

def test_root_and_favicon(api_client):
    client, _ = api_client
    assert client.get("/").status_code == 200
    assert client.get("/favicon.ico").status_code == 204

def test_get_by_tid_found(api_client):
    client, sb = api_client
    data = [{"sid": "S1", "tid": "T1"}]
    sb.fetch_schedule_by_tid.return_value = data
    r = client.get("/tid/T1")
    assert r.status_code == 200
    assert r.json()["data"] == data
    sb.fetch_schedule_by_tid.assert_called_once_with("T1")

def test_get_by_tid_404(api_client):
    client, sb = api_client
    sb.fetch_schedule_by_tid.return_value = None
    r = client.get("/tid/MISS")
    assert r.status_code == 404

def test_get_by_tid_latest_found(api_client):
    client, sb = api_client
    data = {"sid": "S2", "tid": "T2", "created_at": "2025-10-01T00:00:00Z"}
    sb.fetch_schedule_by_tid.return_value = data
    r = client.get("/tid/T2/latest")
    assert r.status_code == 200
    sb.fetch_schedule_by_tid.assert_called_once_with("T2", latest=True)

def test_get_by_tid_latest_404(api_client):
    client, sb = api_client
    sb.fetch_schedule_by_tid.return_value = None
    r = client.get("/tid/T3/latest")
    assert r.status_code == 404

def test_get_by_sid_found(api_client):
    client, sb = api_client
    data = {"sid": "S5", "tid": "T5"}
    sb.fetch_schedule_by_sid.return_value = data
    r = client.get("/sid/S5")
    assert r.status_code == 200
    assert r.json()["data"] == data
    sb.fetch_schedule_by_sid.assert_called_once_with("S5")

def test_get_by_sid_404(api_client):
    client, sb = api_client
    sb.fetch_schedule_by_sid.return_value = None
    r = client.get("/sid/SX")
    assert r.status_code == 404

def test_post_insert_non_recurring(api_client, fake_notify_spies):
    client, sb = api_client
    payload = {
        "tid": "TT1",
        "start": "2025-01-01T00:00:00+00:00",
        "deadline": "2025-01-02T00:00:00+00:00",
        "status": "ongoing",
        "is_recurring": False
    }
    sb.insert_schedule.return_value = {"sid":"SNEW","tid":"TT1"}
    r = client.post("/", json=payload)
    assert r.status_code == 200
    assert fake_notify_spies["added"] == 0  # no notify for non-recurring
    sb.insert_schedule.assert_called_once()

def test_post_insert_recurring_triggers_notify(api_client, fake_notify_spies):
    client, sb = api_client
    payload = {
        "tid": "TT2",
        "start": "2025-02-01T00:00:00+00:00",
        "deadline": "2025-02-02T00:00:00+00:00",
        "status": "ongoing",
        "is_recurring": True,
        "next_occurrence": "2025-02-03T00:00:00+00:00",
        "frequency": "Weekly"
    }
    sb.insert_schedule.return_value = {"sid":"SNEW2","tid":"TT2"}
    r = client.post("/", json=payload)
    assert r.status_code == 200
    assert fake_notify_spies["added"] == 1
    sb.insert_schedule.assert_called_once()

def test_put_update_by_sid_with_cron_change_triggers_notify(api_client, fake_notify_spies):
    client, sb = api_client
    sid = "S9"
    sb.fetch_schedule_by_sid.return_value = {
        "sid": sid, "tid": "T9", "is_recurring": False, "deadline": "2025-03-02T00:00:00+00:00"
    }
    new_data = {"is_recurring": True, "next_occurrence": "2025-03-05T00:00:00+00:00"}
    sb.update_schedule.return_value = {"sid": sid, **new_data}

    r = client.put(f"/{sid}", json=new_data)
    assert r.status_code == 200
    assert fake_notify_spies["updated"] == 1
    sb.fetch_schedule_by_sid.assert_called_once_with(sid)
    sb.update_schedule.assert_called_once_with(sid, new_data)

def test_put_update_by_sid_no_cron_change_no_notify(api_client, fake_notify_spies):
    client, sb = api_client
    sid = "S10"
    sb.fetch_schedule_by_sid.return_value = {"sid": sid, "tid": "T10", "status":"ongoing"}
    new_data = {"status":"overdue"}
    sb.update_schedule.return_value = {"sid": sid, "status":"overdue"}
    r = client.put(f"/{sid}", json=new_data)
    assert r.status_code == 200
    assert fake_notify_spies["updated"] == 0

def test_put_update_by_sid_404_current_missing(api_client):
    client, sb = api_client
    sid = "S404"
    sb.fetch_schedule_by_sid.return_value = None
    r = client.put(f"/{sid}", json={"status":"x"})
    assert r.status_code == 404

def test_put_update_by_sid_404_after_update(api_client):
    client, sb = api_client
    sid = "S404b"
    sb.fetch_schedule_by_sid.return_value = {"sid": sid, "tid": "Tz"}
    sb.update_schedule.return_value = None
    r = client.put(f"/{sid}", json={"status":"x"})
    assert r.status_code == 404

def test_put_update_by_tid_happy_path_with_cron_change(api_client, fake_notify_spies):
    client, sb = api_client
    tid = "TID1"
    sb.fetch_schedule_by_tid.return_value = {"sid":"SID1","tid":tid,"is_recurring":False}
    new_data = {"is_recurring": True, "next_occurrence":"2025-05-01T00:00:00+00:00"}
    sb.update_schedule.return_value = {"sid":"SID1",**new_data}

    r = client.put(f"/tid/{tid}", json=new_data)
    assert r.status_code == 200
    assert fake_notify_spies["updated"] >= 1
    sb.fetch_schedule_by_tid.assert_called_once_with(tid, latest=True)
    sb.update_schedule.assert_called_once_with("SID1", new_data)

def test_put_update_by_tid_404_no_schedule(api_client):
    client, sb = api_client
    tid = "MISSING"
    sb.fetch_schedule_by_tid.return_value = None
    r = client.put(f"/tid/{tid}", json={"status":"any"})
    assert r.status_code == 404

def test_put_update_by_tid_404_no_sid(api_client):
    client, sb = api_client
    tid = "TID2"
    sb.fetch_schedule_by_tid.return_value = {"tid": tid}
    r = client.put(f"/tid/{tid}", json={"status":"any"})
    assert r.status_code == 404

def test_delete_found(api_client):
    client, sb = api_client
    sid = "DEL1"
    sb.delete_schedule.return_value = {"sid": sid}
    r = client.delete(f"/{sid}")
    assert r.status_code == 200
    sb.delete_schedule.assert_called_once_with(sid)

def test_delete_404(api_client):
    client, sb = api_client
    sb.delete_schedule.return_value = None
    r = client.delete("/DELX")
    assert r.status_code == 404

def test_get_recurring_all_ok(api_client):
    client, sb = api_client
    sb.fetch_recurring_tasks.return_value = [{"sid":"S1","tid":"T1"}]
    r = client.get("/recurring/all")
    assert r.status_code == 200
    assert r.json()["tasks"] == [{"sid":"S1","tid":"T1"}]

def test_get_recurring_all_error(api_client):
    client, sb = api_client
    sb.fetch_recurring_tasks.side_effect = Exception("boom")
    r = client.get("/recurring/all")
    assert r.status_code == 400
    assert r.json()["detail"] == "boom"

def test_has_cron_affecting_changes_true():
    from backend.services.atomic.schedule.main import has_cron_affecting_changes
    old_data = {"is_recurring": False, "deadline": "2025-01-01"}
    new_data = {"is_recurring": True}  # change in cron-affecting field
    assert has_cron_affecting_changes(old_data, new_data) is True
    
def test_has_cron_affecting_changes_false():
    from backend.services.atomic.schedule.main import has_cron_affecting_changes
    old_data = {"is_recurring": False, "deadline": "2025-01-01"}
    new_data = {"status": "ongoing"}  # not a cron-affecting field
    assert has_cron_affecting_changes(old_data, new_data) is False

def test_post_insert_recurring_missing_next_occurrence_400(api_client, fake_notify_spies):
    client, sb = api_client
    
