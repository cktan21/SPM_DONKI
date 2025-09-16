from fastapi import FastAPI, HTTPException, Body, Path
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn

from datetime import datetime, timezone
from typing import Any, Dict

load_dotenv()

app = FastAPI(title="Atomic Microservice: Task Service")
supabase = SupabaseClient()

@app.get("/")
def read_root():
    return {"message": "Task Service is running 🚀😱"}

#Create task 
@app.post("/tasks", summary="Create a new task")
async def create_task(
    task: Dict[str, Any] = Body(
        ...,
        example={
            "name": "New Task Title",
            "desc": "Optional description",
            "notes": "Optional notes",
            "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6"  # User ID
        }
    )
):
    # Ensure task has a valid name
    if "name" not in task or task["name"].strip() == "":
        raise HTTPException(status_code=400, detail="Task name is required")
    
    # Required server-side defaults
    # if "status" not in task or task["status"]=="":
    #     task["status"] = "not_started"

    task["updated_timestamp"] = datetime.now(timezone.utc).isoformat()

    # Insert task into Supabase
    resp = supabase.client.table("TASK").insert(task).execute()
    rows = getattr(resp, "data", None) or []

    if not rows:
        raise HTTPException(status_code=400, detail="Failed to create task")

    return {"message": "Task created successfully", "task": rows[0]}

# Update task details
@app.put("/{task_id}", summary="Update a task", response_description="Updated task row")
async def update_task(
    task_id: str = Path(..., description="Primary key of the task (uuid)"),
    updates: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Complete Project Setup",
            "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
            "collaborators": ["3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001", "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Set up the initial project structure and dependencies",
            "notes": "Remember to update the README file"
        }
    ),
):
    # Filter to only allow specific fields
    allowed_fields = {"name", "parentTaskId", "collaborators", "pid", "desc", "notes"}

    # filtered_updates --> dictionary with only allowed fields
    filtered_updates = {}
    for key, value in updates.items():
        if key in allowed_fields:
            # Update the value for the key
            filtered_updates[key] = value
    
    # Add server-side timestamp
    filtered_updates["updated_timestamp"] = datetime.now(timezone.utc).isoformat()
    
    # Use supabaseClient's update_task method
    resp = supabase.update_task(task_id, filtered_updates)
    rows = getattr(resp, "data", None) or []
    
    if not rows:
        raise HTTPException(status_code=404, detail="Task not found or not permitted")
    
    return {"message": "Task updated successfully", "task": rows[0]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)
