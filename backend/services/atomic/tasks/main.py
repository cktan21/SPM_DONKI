from fastapi import FastAPI, HTTPException, Body, Path, Request
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn
from postgrest.exceptions import APIError

from datetime import datetime, timezone
from typing import Any, Dict

load_dotenv()

app = FastAPI(title="Atomic Microservice: Task Service")
supabase = SupabaseClient()

@app.get("/")
def read_root():
    return {"message": "Task Service is running 🚀😱"}

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

#Get All tasks
@app.get("/tasks", summary="Get all tasks")
async def get_all_tasks():
    tasks = supabase.get_all_tasks()
    return {"message": f"{len(tasks)} task(s) retrieved", "tasks": tasks}

# Get task by task ID
@app.get("/{task_id}", summary="Get a task by ID", response_description="Task row")
async def get_task(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    # Query the TASK table by task_id
    resp = (
        supabase.client.table("TASK")
        .select("*")
        .eq("id", task_id)
        .execute()
    )
    rows = getattr(resp, "data", None) or []

    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task retrieved successfully", "task": rows[0]}

#Create task 
@app.post("/createTask", summary="Create a new task")
async def create_task(
    task: Dict[str, Any] = Body(
        ...,
        example={
            "name": "New Task Title",
            "desc": "Optional description",
            "notes": "Optional notes",
            "created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
            "priorityLevel": 8,  # Optional
        }
    )
):
    # Validation
    if "name" not in task or task["name"].strip() == "":
        raise HTTPException(status_code=400, detail="Task name is required")
    if "created_by_uid" not in task:
        raise HTTPException(status_code=400, detail="Task Owner ID is required")

    #Default timestam
    task["updated_timestamp"] = datetime.now(timezone.utc).isoformat()

    # --- Priority logic ---
    level = int(task.get("priorityLevel", 5))  # Default 5
    task["priorityLevel"] = max(1, min(level, 10))  # Clamp 1–10
    task["priorityLabel"] = (
        "High" if level >= 8 else "Medium" if level >= 4 else "Low"
    )

    try:
        resp = supabase.client.table("TASK").insert(task).execute()
        rows = getattr(resp, "data", None) or []

        if not rows:
            raise HTTPException(status_code=400, detail="Failed to create task")

        return {"message": "Task created successfully", "task": rows[0]}

    except APIError as e:
        # Duplicate name error from Supabase/Postgres
        if "duplicate key value" in str(e):
            print("Task name already exist")  # ✅ Logs to backend console
            raise HTTPException(status_code=400, detail="Task name already exist")
        else:
            print("Supabase API error:", str(e))
            raise HTTPException(status_code=500, detail="Database error")

    except Exception as e:
        print("Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail="Unexpected error")


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
    allowed_fields = {"name", "parentTaskId", "collaborators", "pid", "desc", "notes",
                       "priorityLevel", "priorityLabel"}

    # filtered_updates --> dictionary with only allowed fields
    filtered_updates = {}
    for key, value in updates.items():
        if key in allowed_fields:
            # Update the value for the key
            filtered_updates[key] = value

    # --- Priority logic ---
    if "priorityLevel" in filtered_updates:
        level = int(filtered_updates["priorityLevel"])
        filtered_updates["priorityLevel"] = max(1, min(level, 10))
        filtered_updates["priorityLabel"] = (
            "High" if level >= 8 else "Medium" if level >= 4 else "Low"
        )
    
    # Add server-side timestamp
    filtered_updates["updated_timestamp"] = datetime.now(timezone.utc).isoformat()
    
    # Use supabaseClient's update_task method
    resp = supabase.update_task(task_id, filtered_updates)
    rows = getattr(resp, "data", None) or []
    
    if not rows:
        raise HTTPException(status_code=404, detail="Task not updated")
    
    return {"message": "Task updated successfully", "task": rows[0]}

#Delete Task
@app.delete("/{task_id}", summary="Delete a task")
async def delete_task(
    task_id: str = Path(..., description="ID of the task to delete"),
):
    """
    Delete a task by its ID only.
    """
    # Call Supabase delete by task_id
    resp = supabase.delete_task(task_id)
    rows = getattr(resp, "data", None) or []

    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully", "task": rows[0]}

# @app.delete("/{task_id}", summary="Delete a task")
# async def delete_task(
#     task_id: str = Path(..., description="ID of the task to delete"),
#     request: Request = None
# ):
#     """
#     Delete a task. User ID must be passed as a query parameter:
#     /{task_id}?user_id=<current_user_id>
#     """
#     # Get user_id from query params
#     user_id = request.query_params.get("user_id")
    
#     if not user_id:
#         raise HTTPException(status_code=400, detail="User ID is required")  
    
#     resp = supabase.delete_task(task_id, user_id)
#     rows = getattr(resp, "data", None) or []

#     if not rows:
#         raise HTTPException(status_code=404, detail="Task not found or not permitted")

#     return {"message": "Task deleted successfully", "task": rows[0]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)
