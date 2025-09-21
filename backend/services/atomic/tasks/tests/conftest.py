# tests/conftest.py
import sys
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pytest
from fastapi.testclient import TestClient

# --- Make sure Python can import main.py and supabaseClient.py ---
# tasks/
#   main.py
#   supabaseClient.py
#   tests/conftest.py  (this file)
TASKS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TASKS_DIR))  # so 'import main' and 'import supabaseClient' work

import main  # now resolves main.py and its 'from supabaseClient import SupabaseClient'

# ---------- Supabase fakes ----------
class FakeResponse:
    def __init__(self, data: Optional[List[Dict[str, Any]]]):
        self.data = data

class _FakeQuery:
    def __init__(self, store, table_name):
        self._store = store
        self._table = table_name
        self._filters = {}
        self._is_select = False
        self._single = False
        self._pending_insert = None

    def insert(self, row: Dict[str, Any]):
        self._pending_insert = row
        return self

    def select(self, *args, **kwargs):
        self._is_select = True
        return self

    def eq(self, column: str, value: Any):
        self._filters[column] = value
        return self

    def single(self):
        self._single = True
        return self

    def execute(self):
        # INSERT
        if self._pending_insert is not None:
            if self._store.flags.get("force_insert_empty", False):
                return FakeResponse(data=[])
            row = dict(self._pending_insert)
            row.setdefault("id", str(uuid.uuid4()))
            now = datetime.now(timezone.utc).isoformat()
            row.setdefault("created_timestamp", now)
            row.setdefault("updated_timestamp", now)
            self._store.tables.setdefault(self._table, {})
            self._store.tables[self._table][row["id"]] = row
            return FakeResponse(data=[row])

        # SELECT
        if self._is_select:
            items = list(self._store.tables.get(self._table, {}).values())
            for k, v in self._filters.items():
                items = [it for it in items if it.get(k) == v]
            if self._single:
                if not items:
                    return FakeResponse(data=None)
                return FakeResponse(data=items[0])
            return FakeResponse(data=items)

        return FakeResponse(data=[])

class _FakeTableAPI:
    def __init__(self, store, table_name):
        self._store = store
        self._table = table_name

    def insert(self, row: Dict[str, Any]):
        return _FakeQuery(self._store, self._table).insert(row)

    def select(self, *args, **kwargs):
        return _FakeQuery(self._store, self._table).select(*args, **kwargs)

class _FakeClient:
    def __init__(self, store):
        self._store = store

    def table(self, table_name: str):
        return _FakeTableAPI(self._store, table_name)

class FakeSupabase:
    def __init__(self):
        self.tables = {}  # {table: {id: row}}
        self.client = _FakeClient(self)
        self.flags = {"force_insert_empty": False, "force_update_empty": False}

    def update_task(self, task_id: str, updates: Dict[str, Any]):
        if self.flags.get("force_update_empty", False):
            return FakeResponse(data=[])
        task_tbl = self.tables.get("TASK", {})
        row = task_tbl.get(task_id)
        if not row:
            return FakeResponse(data=[])
        row.update(updates)
        task_tbl[task_id] = row
        return FakeResponse(data=[row])

    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self.tables.get("TASK", {}).get(task_id)

# ---------- Fixtures ----------
@pytest.fixture(autouse=True)
def fake_supabase(monkeypatch):
    fake = FakeSupabase()
    # Replace the global supabase used in main.py routes
    monkeypatch.setattr(main, "supabase", fake, raising=True)
    return fake

@pytest.fixture
def client():
    return TestClient(main.app)
