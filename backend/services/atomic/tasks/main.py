from fastapi import FastAPI, HTTPException, Body, Path, Request
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn
from postgrest.exceptions import APIError
from datetime import datetime, timezone
from typing import Any, Dict, List
import os
import logging
import pytz
from fastapi.middleware.cors import CORSMiddleware
from kafka_client import KafkaEventPublisher, EventTypes, Topics
from datetime import datetime
import uuid

from pydantic import BaseModel

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

app = FastAPI(title="Atomic Microservice: Task Service")
supabase = SupabaseClient()

# Initialize Kafka publisher
kafka_publisher = KafkaEventPublisher()

# CORS
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
_env_origins = os.getenv("CORS_ORIGINS")
allowed_origins = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins else DEFAULT_ORIGINS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # set False if you don't use cookies/auth
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Internal-API-Key",  # custom header used by /internal calls
        "*",
    ],
    expose_headers=["*"],
    max_age=600,
)

class TimeEntryCreate(BaseModel):
    hours: int
    minutes: int
    description: str = ""

class TimeEntry(BaseModel):
    id: str
    hours: int
    minutes: int
    description: str
    date: str
    userId: str
    userName: str

# Helper function to notify task participants
def notify_task_participants(task_id, event_type: str, task_data: Dict[str, Any], 
                                 updated_fields: List[str] = None, participants: List[Dict[str, Any]] = None) -> bool:
    """
    Notify all task participants about task events via Kafka
    """
    try:
        logger.info(f"🚀 Starting notification process for task {task_id}, event: {event_type}")
        
        # Ensure Kafka producer is connected
        if not kafka_publisher.producer:
            logger.info("📡 Connecting to Kafka producer...")
            kafka_publisher._connect()
            if not kafka_publisher.producer:
                logger.error("❌ Failed to initialize Kafka producer")
                return False
        
        # Get all participants for this task
        logger.info(f"👥 Fetching participants for task {task_id}")
        
        logger.info(f"Participants data: {participants}")
        
        if not participants:
            logger.warning(f"⚠️ No participants found for task {task_id}")
            return False
        
        logger.info(f"✅ Found {len(participants)} participants for task {task_id}")
        
        # Prepare event data
        event_data = {
            "tid": task_id,
            "task_name": task_data.get("name", "Unknown Task"),
            "description": task_data.get("desc", ""),
            "priority_level": task_data.get("priorityLevel", 0),
            "label": task_data.get("label", ""),
            "project_id": task_data.get("pid"),
            "created_by_uid": task_data.get("created_by_uid"),
            "collaborators": task_data.get("collaborators", []),
            "timestamp": datetime.now(UTC_PLUS_8).isoformat()
        }
        
        # Add updated fields for update events
        if updated_fields:
            event_data["updated_fields"] = updated_fields
        
        logger.info(f"📝 Prepared event data: {event_data}")
        
        # Send events to all participants
        failed_count = 0
        success_count = 0
        
        for i, participant in enumerate(participants):
            logger.info(f"📤 Sending notification {i+1}/{len(participants)} to participant {participant.get('user_id')}")
            
            local_event_data = event_data.copy()
            local_event_data["uid"] = participant.get("user_id")
            local_event_data["name"] = participant.get("user_name")
            local_event_data["email"] = participant.get("user_email")
            local_event_data["role"] = participant.get("user_role")
            local_event_data["department"] = participant.get("department")
            local_event_data["phone"] = participant.get("phone")
            local_event_data["is_creator"] = participant.get("is_creator", False)
            local_event_data["is_collaborator"] = participant.get("is_collaborator", False)
            
            logger.debug(f"📋 Participant data: {local_event_data}")
            
            # Publish event for each participant
            success = kafka_publisher.publish_event(
                topic=Topics.NOTIFICATION_EVENTS,
                event_type=event_type,
                data=local_event_data,
            )
            
            if success:
                success_count += 1
                logger.info(f"✅ Successfully sent notification to participant {participant.get('user_id')}")
            else:
                failed_count += 1
                logger.error(f"❌ Failed to send notification to participant {participant.get('user_id')}")
        
        # Final flush to ensure all messages are sent
        try:
            logger.info("🔄 Flushing remaining Kafka messages...")
            kafka_publisher.producer.flush(timeout=10)
            logger.info("✅ Kafka flush completed")
        except Exception as e:
            logger.error(f"❌ Error during Kafka flush: {e}")
        
        if failed_count > 0:
            logger.error(f"❌ Failed to broadcast {failed_count} out of {len(participants)} task events")
            return False
        
        logger.info(f"🎉 Successfully broadcasted task events for {success_count} participants")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error notifying task participants: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

@app.get("/")
def read_root():
    return {"message": "Task Service is running 🚀😱"}

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

#Get All tasks
@app.get("/tasks", summary="Get all tasks")
async def get_all_tasks(sortBy: str = None, filter: str = None):
    """
    Fetch all tasks, with optional filtering and sorting.
    Query params:
      - sortBy: priority | deadline | status
      - filter: comma-separated key:value, e.g. "deadline:upcoming,status:incomplete"
    """
    tasks = supabase.get_all_tasks()
    
    # ---- Apply filtering ----
    if filter:
        filters = dict(item.split(":") for item in filter.split(",") if ":" in item)
        filtered_tasks = []
        for task in tasks:
            include = True

            # Filter by deadline
            if "deadline" in filters:
                now = datetime.now(timezone.utc)
                deadline_str = task.get("deadline")  # assume string in ISO format
                if deadline_str:
                    try:
                        deadline_dt = datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
                        if filters["deadline"] == "upcoming" and not (0 <= (deadline_dt - now).days <= 3):
                            include = False
                        elif filters["deadline"] == "overdue" and not (deadline_dt < now):
                            include = False
                    except Exception:
                        include = False
                else:
                    include = False

            # Filter by status
            if "status" in filters:
                status = task.get("status", "").lower()
                if filters["status"].lower() != status:
                    include = False

            if include:
                filtered_tasks.append(task)
        tasks = filtered_tasks

    # ---- Apply sorting ----
    if sortBy:
        sort_key = sortBy.lower()
        if sort_key == "priority":
            tasks.sort(key=lambda x: x.get("priorityLevel", 0), reverse=True)
        elif sort_key == "deadline":
            def parse_deadline(t):
                try:
                    return datetime.fromisoformat(t.get("deadline","").replace("Z","+00:00"))
                except Exception:
                    return datetime.max
            tasks.sort(key=parse_deadline)
        elif sort_key == "status":
            # Example: incomplete < complete
            status_order = {"incomplete": 0, "complete": 1}
            tasks.sort(key=lambda x: status_order.get(x.get("status","incomplete").lower(), 0))

    return {"message": f"{len(tasks)} task(s) retrieved", "tasks": tasks}

# Get task by task ID
@app.get("/tid/{task_id}", summary="Get a task by its ID", response_description="Task row")
async def get_task(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    rows = supabase.get_all_tasks(filter_by={"id": task_id})
    if not rows:
        return {"message": "Task not found", "task": None}
    
    task = rows[0]

    # Fetch subtasks
    subtasks = supabase.get_all_tasks(filter_by={"parentTaskId": task_id})
    task["subtasks"] = subtasks or []

    # ✅ Return the modified task object
    return {"message": "Task retrieved successfully", "task": task}

# Get task by project ID
@app.get("/pid/{project_id}", summary="Get all tasks by project ID")
async def get_tasks_by_project(
    project_id: str = Path(..., description="Project ID")
):
    tasks = supabase.get_all_tasks(filter_by={"pid": project_id})
    if not tasks:
        return {"message": "No tasks found for this project", "tasks": []}
    return {"message": f"{len(tasks)} task(s) retrieved", "tasks": tasks}


# Get task by parent Task ID
@app.get("/ptid/{parent_task_id}", summary="Get all tasks by parent Task ID")
async def get_tasks_by_parent_task(
    parent_task_id: str = Path(..., description="Parent Task ID")
):
    tasks = supabase.get_all_tasks(filter_by={"parentTaskId": parent_task_id})
    if not tasks:
        return {"message": "No children tasks found for this parent task", "tasks": []}
    return {"message": f"{len(tasks)} children task(s) retrieved", "tasks": tasks}

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

    try:
        resp = supabase.client.table("TASK").insert(task).execute()
        rows = getattr(resp, "data", None) or []

        if not rows:
            raise HTTPException(status_code=400, detail="Failed to create task")

        return {"message": "Task created successfully", "task": rows[0]}

    except APIError as e:
        # Handle database errors - duplicate names are now allowed
        # If you still get duplicate key errors, remove the unique constraint from the database
        error_str = str(e).lower()
        if "duplicate key value" in error_str:
            logger.error(f"Database constraint violation (may need to remove unique constraint): {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Database constraint error. If this is about duplicate task names, please remove the UNIQUE constraint on the 'name' field in the TASK table: {str(e)}"
            )
        else:
            logger.error(f"Supabase API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# Update task details
@app.put("/{task_id}", summary="Update a task", response_description="Updated task row")
async def update_task(
    task_id = Path(..., description="Primary key of the task (UUID)"),
    updates: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Complete Project Setup",
            "parentTaskId": "16e2b6cc-fb44-4873-9292-b8c697832a2e",
            "collaborators": ["3e3b2d6c-6d6b-4dc0-9b76-0b6b3fe9c001", "f7f5cf6e-1c3a-4d3a-8d50-5a2f60d9a002"],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Set up the initial project structure and dependencies",
            "notes": "Remember to update the README file",
            "priorityLevel": 2,
            "label": "Setup"
        }
    ),
):
    # Add server-side timestamp
    updates["updated_timestamp"] = datetime.now(timezone.utc).isoformat()
    
    # Get current task data before update for notifications
    current_task = None
    try:
        current_resp = supabase.get_task_participants(task_id)
        if current_resp and hasattr(current_resp, 'data') and current_resp.data:
            current_task = current_resp.data[0] if isinstance(current_resp.data, list) else current_resp.data
    except Exception as e:
        logger.warning(f"Could not fetch current task data for notifications: {e}")
    
    # Use supabaseClient's update_task method
    resp = supabase.update_task(task_id, updates)
    rows = getattr(resp, "data", None) or []
    
    if not rows:
        raise HTTPException(status_code=404, detail="Task not updated")
    
    updated_task = rows[0]
    
    # Send notifications to all task participants (excluding collaborator-only changes)
    try:
        # Check if only collaborators field was updated
        only_collaborators_changed = (
            "collaborators" in updates and 
            len(updates.keys()) == 1
        )
        
        if not only_collaborators_changed:
            # Get updated fields for notification
            updated_fields = list(updates.keys())
            if "updated_timestamp" in updated_fields:
                updated_fields.remove("updated_timestamp")
            participants = supabase.get_task_participants(task_id)
            # Send notification
            notification_success = notify_task_participants(
                task_id=task_id,
                event_type=EventTypes.TASK_UPDATED,
                task_data=updated_task,
                updated_fields=updated_fields,
                participants=participants
            )
            
            if notification_success:
                logger.info(f"✅ Successfully notified participants about task {task_id} update")
            else:
                logger.warning(f"⚠️ Failed to notify some participants about task {task_id} update")
        else:
            logger.info(f"ℹ️ Skipping notification for task {task_id} - only collaborators field updated")
            
    except Exception as e:
        logger.error(f"❌ Error sending task update notifications: {str(e)}")
        # Don't fail the update if notifications fail
    
    return {"message": "Task updated successfully", "task": updated_task}


#Delete Task
@app.delete("/{task_id}", summary="Delete a task")
async def delete_task(
    task_id: str = Path(..., description="ID of the task to delete"),
):
    """
    Delete a task by its ID only.
    """
    # Get task data before deletion for notifications
    task_data = None
    try:
        task_data = supabase.get_task(task_id)
        if task_data:
            logger.info(f"Retrieved task data for deletion notifications: {task_data.get('name', 'Unknown')}")
        else:
            logger.warning(f"No task data found for task {task_id}")
    except Exception as e:
        logger.warning(f"Could not fetch task data for notifications: {e}")
        
    participants = supabase.get_task_participants(task_id)
    
    # Call Supabase delete by task_id
    resp = supabase.delete_task(task_id)
    rows = getattr(resp, "data", None) or []

    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = rows[0]
    
    # Send notifications to all task participants
    try:
        if task_data:
            notification_success = notify_task_participants(
                task_id=task_id,
                event_type=EventTypes.TASK_DELETED,
                task_data=task_data,
                participants=participants
            )
            
            if notification_success:
                logger.info(f"✅ Successfully notified participants about task {task_id} deletion")
            else:
                logger.warning(f"⚠️ Failed to notify some participants about task {task_id} deletion")
        else:
            logger.warning(f"⚠️ Could not send deletion notifications for task {task_id} - no task data available")
            
    except Exception as e:
        logger.error(f"❌ Error sending task deletion notifications: {str(e)}")
        # Don't fail the deletion if notifications fail

    return {"message": "Task deleted successfully", "task": deleted_task}


@app.get("/tasks/{task_id}/time-entries", summary="Get all time entries for a task")
async def get_task_time_entries(
    task_id: str = Path(..., description="Task ID")
):
    """
    Fetch all time entries for a specific task.
    """
    try:
        # Get task with time_entries column
        resp = supabase.client.table("TASK").select("time_entries").eq("id", task_id).execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Task not found")
        
        time_entries = resp.data[0].get("time_entries", [])
        
        return {
            "message": f"{len(time_entries)} time entry(ies) retrieved",
            "task_id": task_id,
            "time_entries": time_entries
        }
    except Exception as e:
        logger.error(f"Error fetching time entries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch time entries: {str(e)}")


# Add time entry to a task
@app.post("/tasks/{task_id}/time-entries", summary="Add a time entry to a task")
async def add_task_time_entry(
    task_id: str = Path(..., description="Task ID"),
    entry: TimeEntryCreate = Body(...),
    user_id: str = Body(..., embed=True),
    user_name: str = Body(..., embed=True)
):
    """
    Add a new time entry to a task's time log.
    """
    try:
        # Get current time entries
        resp = supabase.client.table("TASK").select("time_entries").eq("id", task_id).execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Task not found")
        
        current_entries = resp.data[0].get("time_entries", [])
        
        # Create new time entry
        new_entry = {
            "id": str(uuid.uuid4()),
            "hours": entry.hours,
            "minutes": entry.minutes,
            "description": entry.description,
            "date": datetime.now(UTC_PLUS_8).isoformat(),
            "userId": user_id,
            "userName": user_name
        }
        
        # Append to existing entries
        updated_entries = current_entries + [new_entry]
        
        # Update task with new time entries
        update_resp = supabase.client.table("TASK").update({
            "time_entries": updated_entries,
            "updated_timestamp": datetime.now(timezone.utc).isoformat()
        }).eq("id", task_id).execute()
        
        if not update_resp.data:
            raise HTTPException(status_code=400, detail="Failed to add time entry")
        
        logger.info(f"✅ Time entry added to task {task_id} by user {user_name}")
        
        return {
            "message": "Time entry added successfully",
            "task_id": task_id,
            "entry": new_entry
        }
        
    except Exception as e:
        logger.error(f"Error adding time entry: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add time entry: {str(e)}")


# Remove time entry from a task
@app.delete("/tasks/{task_id}/time-entries/{entry_id}", summary="Remove a time entry from a task")
async def remove_task_time_entry(
    task_id: str = Path(..., description="Task ID"),
    entry_id: str = Path(..., description="Time entry ID"),
    user_id: str = Body(..., embed=True)
):
    """
    Remove a time entry from a task's time log.
    Only the user who created the entry can delete it.
    """
    try:
        # Get current time entries
        resp = supabase.client.table("TASK").select("time_entries").eq("id", task_id).execute()
        
        if not resp.data:
            raise HTTPException(status_code=404, detail="Task not found")
        
        current_entries = resp.data[0].get("time_entries", [])
        
        # Find and validate the entry
        entry_to_remove = None
        updated_entries = []
        
        for entry in current_entries:
            if entry.get("id") == entry_id:
                # Check if user owns this entry
                if entry.get("userId") != user_id:
                    raise HTTPException(
                        status_code=403, 
                        detail="You can only delete your own time entries"
                    )
                entry_to_remove = entry
            else:
                updated_entries.append(entry)
        
        if not entry_to_remove:
            raise HTTPException(status_code=404, detail="Time entry not found")
        
        # Update task with filtered entries
        update_resp = supabase.client.table("TASK").update({
            "time_entries": updated_entries,
            "updated_timestamp": datetime.now(timezone.utc).isoformat()
        }).eq("id", task_id).execute()
        
        if not update_resp.data:
            raise HTTPException(status_code=400, detail="Failed to remove time entry")
        
        logger.info(f"✅ Time entry {entry_id} removed from task {task_id}")
        
        return {
            "message": "Time entry removed successfully",
            "task_id": task_id,
            "entry_id": entry_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing time entry: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to remove time entry: {str(e)}")



@app.get("/task-participants/{task_id}", summary="Get all participants for a task")
async def get_task_participants(
    task_id: str = Path(..., description="Task ID")
):
    participants = supabase.get_task_participants(task_id)
    if not participants:
        return {"message": "No participants found for this task", "participants": []}
    return {"message": f"{len(participants)} participant(s) retrieved", "participants": participants}

@app.get("/logs", summary="Get all logs")
async def get_all_logs():
    logs = supabase.get_all_logs()
    return {"message": f"{len(logs)} log(s) retrieved", "logs": logs}

@app.get("/logs/{tid}", summary="Get a log by its ID")
async def get_log(
    tid: str = Path(..., description="ID of the log to get"),
):
    log = supabase.get_all_logs(filter_by=tid)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log retrieved successfully", "log": log}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)
