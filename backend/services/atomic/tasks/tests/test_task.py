import uuid
from typing import Any, Dict

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

# --- CREATE TESTS ---

def test_create_tc1_successful_task_creation(client):
    """TC1: Positive: Created new task, successful returns message 'Task created successfully'"""
    print("\n[Create:TC1] Creating a new task (expect success)")
    
    resp = client.post("/tasks", json=sample_create_payload())
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Task created successfully"
    assert "task" in data and "id" in data["task"]
    
    print("[Create:TC1] Positive test case: PASS -> ", data["message"], "ID:", data["task"]["id"], flush=True)

def test_create_tc2_unsuccessful_task_creation(client, fake_supabase):
    """TC2: Negative: Unsuccessful create. Return message 'Failed to create task'"""
    print("\n[Create:TC2] Creating a new task (simulate DB failure)")
    
    # Simulate database failure
    fake_supabase.flags["force_insert_empty"] = True
    
    resp = client.post("/tasks", json=sample_create_payload())
    
    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "Failed to create task"
    
    print("[Create:TC2] Negative test case PASS ->", data["detail"], flush=True)

# --- UPDATE TESTS ---

def test_update_tc1_update_all_fields_success_message(client):
    """TC1: Positive: Update all allowed fields --> check that return message 'Task updated successfully'"""
    print("\n[Update:TC1] Update all allowed fields (expect success message)")
    
    # First create a task
    create_resp = client.post("/tasks", json=sample_create_payload())
    assert create_resp.status_code == 200
    task = create_resp.json()["task"]
    task_id = task["id"]
    
    # Update all allowed fields
    upd = sample_update_payload()
    resp = client.put(f"/{task_id}", json=upd)
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Task updated successfully"
    
    # Verify the returned task data reflects the changes
    updated_task = data["task"]
    assert updated_task["name"] == upd["name"]
    assert updated_task["desc"] == upd["desc"]
    assert updated_task["notes"] == upd["notes"]
    assert updated_task["parentTaskId"] == upd["parentTaskId"]
    assert updated_task["pid"] == upd["pid"]
    assert updated_task["collaborators"] == upd["collaborators"]
    
    print("[Update:TC1] Positive test case: PASS ->", data["message"], "- All fields verified in response", flush=True)


def test_update_tc2_update_failed_message(client, fake_supabase):
    """TC2: Negative: Update failed --> check that return message 'Task not updated'"""
    print("\n[Update:TC3] Update non-existent task (expect failure message)")
    
    # Use a non-existent task ID
    non_existent_id = str(uuid.uuid4())
    
    # Simulate update failure
    fake_supabase.flags["force_update_empty"] = True
    
    resp = client.put(f"/{non_existent_id}", json=sample_update_payload())
    
    assert resp.status_code == 404
    data = resp.json()
    assert data["detail"] == "Task not updated"
    
    print("[Update:TC2] Negative test case: PASS ->", data["detail"], flush=True)