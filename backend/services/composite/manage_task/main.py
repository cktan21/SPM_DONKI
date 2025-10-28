from fastapi import FastAPI, HTTPException, Path, Body
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import logging
import pytz

from fastapi.middleware.cors import CORSMiddleware
from kafka_client import KafkaEventPublisher, EventTypes, Topics


load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

# Initialize Kafka publisher
kafka_publisher = KafkaEventPublisher()

app = FastAPI(title="Composite Microservice: manage-task Service")

DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
_env_origins = os.getenv("CORS_ORIGINS")
allowed_origins = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins
    else DEFAULT_ORIGINS
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


# Configuration for external services
TASK_SERVICE_URL = "http://tasks:5500"
USERS_SERVICE_URL = "http://user:5100"
PROJECTS_SERVICE_URL = "http://project:5200"
SCHEDULE_SERVICE_URL = "http://schedule:5300"

# for validating user
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

async def get_task_participants(task_id) -> List[Dict[str, Any]]:
    """
    Get all participants (creator + collaborators) for a task using the task_participants view
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Query the schedule_participants view to get all participants for this task
            response = await client.get(
                f"{TASK_SERVICE_URL}/task-participants/{task_id}",
                headers={"X-Internal-API-Key": INTERNAL_API_KEY}
            )
            
            if response.status_code == 200:
                participants_data = response.json()
                participants_data = participants_data.get("participants", [])
                logger.info(f"Retrieved participants for task {task_id}: {participants_data}")
                return participants_data
            else:
                logger.error(f"Failed to get participants for task {task_id}: {response.status_code}")
                return []
    except Exception as e:
        logger.error(f"Error getting participants for task {task_id}: {str(e)}")
        return []

def test_kafka_connectivity() -> bool:
    """
    Test Kafka connectivity and topic existence
    """
    try:
        logger.info("🔍 Testing Kafka connectivity...")
        
        # Test producer connection
        if not kafka_publisher.producer:
            kafka_publisher._connect()
        
        if not kafka_publisher.producer:
            logger.error("❌ Failed to create Kafka producer")
            return False
        
        logger.info("✅ Kafka producer created successfully")
        
        # Test sending a simple message
        test_event = {
            'event_type': 'test_connectivity',
            'timestamp': datetime.now(UTC_PLUS_8).isoformat(),
            'data': {'test': True, 'message': 'Kafka connectivity test'}
        }
        
        logger.info("📤 Sending test message to Kafka...")
        success = kafka_publisher.publish_event(
            topic=Topics.NOTIFICATION_EVENTS,
            event_type="test_connectivity",
            data={'test': True, 'message': 'Kafka connectivity test'}
        )
        
        if success:
            logger.info("✅ Kafka connectivity test successful!")
            return True
        else:
            logger.error("❌ Kafka connectivity test failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Kafka connectivity test error: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

async def notify_task_participants(task_id, task_data: Dict[str, Any]) -> bool:
    """
    Notify all task participants (creator + collaborators) about task assignment via Kafka
    """
    try:
        logger.info(f"🚀 Starting notification process for task {task_id}")
        
        # Ensure Kafka producer is connected
        if not kafka_publisher.producer:
            logger.info("📡 Connecting to Kafka producer...")
            kafka_publisher._connect()
            if not kafka_publisher.producer:
                logger.error("❌ Failed to initialize Kafka producer")
                return False
        
        # Get all participants for this task
        logger.info(f"👥 Fetching participants for task {task_id}")
        participants = await get_task_participants(task_id)
        
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
            "status": "assigned",
            "timestamp": datetime.now(UTC_PLUS_8).isoformat()
        }
        
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
                event_type=EventTypes.TASK_ASSIGNED,
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
            logger.error(f"❌ Failed to broadcast {failed_count} out of {len(participants)} task assignment events")
            return False
        
        logger.info(f"🎉 Successfully broadcasted task assignment events for {success_count} participants")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error notifying task participants: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Composite Manage Task Service is running 🚀",
        "service": "manage-task-composite",
    }

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Favicon handler
@app.get("/favicon.ico")
async def get_favicon():
    from fastapi.responses import Response

    return Response(status_code=204)


# Composite endpoints
@app.get(
    "/tasks/user/{user_id}",
    summary="Get all tasks where user is a collaborator",
    response_description="List of tasks with enriched details where user is a collaborator (+ user name)",
)
async def get_tasks_by_user_composite(
    user_id: str = Path(
        ..., description="User ID to fetch tasks for (where user is a collaborator)"
    )
):
    """
    Composite endpoint:
    1. Fetch all tasks from Task MS
    2. Filter tasks where user_id is in collaborators
    3. Enrich each task with schedule and project data
    4. Flatten key schedule fields (status, deadline) directly into task object
    5. Nest subtasks under parent tasks
    6. Fetch user's display name from Users MS and include in response
    """
    async with httpx.AsyncClient() as client:
        try:
            # ---- 0) Fetch user info (for name) ----
            user_name: str | None = None
            try:
                user_resp = await client.get(f"{USERS_SERVICE_URL}/internal/{user_id}")
                if user_resp.status_code == 200:
                    u = user_resp.json() or {}
                    if u.get("name"):
                        user_name = u["name"]
                    elif u.get("email"):
                        user_name = u["email"].split("@")[0]
                    else:
                        user_name = user_id
                else:
                    user_name = user_id
            except Exception:
                user_name = user_id

            # ---- 1) Get all tasks from Task MS ----
            print(f"Fetching tasks from: {TASK_SERVICE_URL}/tasks")
            tasks_response = await client.get(f"{TASK_SERVICE_URL}/tasks")
            tasks_response.raise_for_status()
            response_data = tasks_response.json()
            print(f"Received response: {response_data}")

            all_tasks = response_data.get("tasks", [])
            if not isinstance(all_tasks, list):
                raise HTTPException(
                    status_code=500, detail="Unexpected response format from Task MS"
                )

            print(f"Total tasks found: {len(all_tasks)}")

            # ---- 2) Filter tasks where user_id is in collaborators ----
            user_tasks = []
            for task in all_tasks:
                collaborators = task.get("collaborators")
                print(f"Task {task.get('id')}: collaborators = {collaborators}")
                if (
                    collaborators
                    and isinstance(collaborators, list)
                    and user_id in collaborators
                ):
                    user_tasks.append(task)
                    print(f"✓ User {user_id} found in task {task.get('id')}")

            print(f"Total user tasks found: {len(user_tasks)}")

            if not user_tasks:
                return {
                    "user_id": user_id,
                    "user": {"id": user_id, "name": user_name},
                    "tasks": [],
                    "count": 0,
                    "message": "No tasks found where user is a collaborator",
                    "metadata": {
                        "retrieved_at": datetime.now(timezone.utc).isoformat(),
                        "total_tasks_checked": len(all_tasks),
                    },
                }

            # ---- 3) Enrich each task with schedule and project data ----
            enriched_tasks = []
            for task in user_tasks:
                task_id = task.get("id")

                # schedule - extract status and deadline
                schedule_status = None
                schedule_deadline = None
                try:
                    schedule_response = await client.get(
                        f"{SCHEDULE_SERVICE_URL}/tid/{task_id}/latest"
                    )
                    if schedule_response.status_code == 200:
                        schedule_resp = schedule_response.json()
                        schedule_data = schedule_resp.get("data", schedule_resp)
                        schedule_status = schedule_data.get("status")
                        schedule_deadline = schedule_data.get("deadline")
                except Exception:
                    pass

                # project
                project_data = None
                if task.get("pid"):
                    try:
                        project_response = await client.get(
                            f"{PROJECTS_SERVICE_URL}/pid/{task['pid']}"
                        )
                        if project_response.status_code == 200:
                            project_data = project_response.json()
                    except Exception:
                        project_data = {"message": "Project information unavailable"}

                # Calculate deadline flag
                deadline_flag = None
                if schedule_deadline:
                    try:
                        deadline_dt = datetime.fromisoformat(
                            schedule_deadline.replace("Z", "+00:00")
                        )
                        now = datetime.now(timezone.utc)

                        if schedule_status != "complete":
                            if now > deadline_dt:
                                deadline_flag = "Overdue"
                            elif 0 <= (deadline_dt - now).days <= 3:
                                deadline_flag = "Upcoming"
                    except Exception:
                        deadline_flag = None

                # Build enriched task with status and deadline inside task object
                enriched_task = {
                    "task": {
                        **task,
                        "status": schedule_status,
                        "deadline": schedule_deadline,
                    },
                    "project": project_data,
                    "deadline_flag": deadline_flag,
                }

                enriched_tasks.append(enriched_task)

            # ✅ 5) NEST SUBTASKS UNDER PARENT TASKS
            task_map = {t["task"]["id"]: t for t in enriched_tasks}
            nested_tasks = []

            for entry in enriched_tasks:
                task = entry["task"]
                parent_id = task.get("parentTaskId")
                if parent_id and parent_id in task_map:
                    parent_entry = task_map[parent_id]
                    parent_entry.setdefault("subtasks", []).append(entry)
                else:
                    nested_tasks.append(entry)

            # ---- 5b) COMPUTE PROGRESS FOR TASKS WITH SUBTASKS ----
            for entry in nested_tasks:
                subtasks = entry.get("subtasks", [])
                if subtasks:
                    total = len(subtasks)
                    completed = sum(
                        1 for sub in subtasks if sub["task"].get("status") == "complete"
                    )
                    entry["task"]["progress"] = round((completed / total) * 100, 2)

            # ✅ 6) Return with nested tasks and user info
            return {
                "user_id": user_id,
                "user": {"id": user_id, "name": user_name},
                "tasks": nested_tasks,
                "count": len(nested_tasks),
                "metadata": {
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "total_tasks_checked": len(all_tasks),
                },
            }

        except httpx.HTTPStatusError as e:
            print(f"HTTPStatusError: {e}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Task MS returned an error: {e.response.text}",
            )
        except httpx.RequestError as e:
            print(f"RequestError: {e}")
            raise HTTPException(
                status_code=503, detail=f"Failed to connect to services: {str(e)}"
            )
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )


@app.get(
    "/tasks/{task_id}",
    summary="Get full task details (composite)",
    response_description="Returns task with schedule, project, creator, collaborators, and parent task names",
)
async def get_task_composite(
    task_id: str = Path(..., description="UUID of the task to retrieve")
):
    """
    Composite endpoint:
    1. Fetch task from Task MS (unwrap inner task object if needed)
    2. Fetch schedule info from Schedule MS
    3. Fetch project name via pid (from Project MS)
    4. Fetch creator name via created_by_uid (from Users MS)
    5. Fetch collaborators[] names via User MS
    6. Fetch parent task name if parentTaskId exists
    """

    async with httpx.AsyncClient() as client:
        try:
            # === 1. Get Task ===
            task_resp = await client.get(f"{TASK_SERVICE_URL}/tid/{task_id}")
            if task_resp.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            task_resp.raise_for_status()

            raw_task = task_resp.json()
            task_data = raw_task.get("task", raw_task)
            if not isinstance(task_data, dict):
                raise HTTPException(
                    status_code=500, detail="Invalid task format from Task MS"
                )

            # === 2. Get Schedule ===
            schedule_status = None
            schedule_deadline = None
            schedule_start = None  # NEW
            schedule_is_recurring = None  # NEW
            schedule_frequency = None  # NEW
            schedule_next_occurrence = None  # NEW
            try:
                s_resp = await client.get(
                    f"{SCHEDULE_SERVICE_URL}/tid/{task_id}/latest"
                )
                if s_resp.status_code == 200:
                    schedule_resp = s_resp.json()
                    schedule_data = schedule_resp.get("data", schedule_resp)
                    schedule_status = schedule_data.get("status")
                    schedule_deadline = schedule_data.get("deadline")
                    schedule_start = schedule_data.get("start")  # NEW
                    schedule_is_recurring = schedule_data.get("is_recurring")  # NEW
                    schedule_frequency = schedule_data.get("frequency")  # NEW
                    schedule_next_occurrence = schedule_data.get("next_occurrence")  # NEW
            except Exception:
                pass

            # === 3. Get Project (by pid) ===
            project_obj = None
            if task_data.get("pid"):
                try:
                    pr_resp = await client.get(
                        f"{PROJECTS_SERVICE_URL}/pid/{task_data['pid']}"
                    )
                    if pr_resp.status_code == 200:
                        pr_json = pr_resp.json()
                        project_obj = {
                            "id": pr_json.get("id", task_data["pid"]),
                            "name": pr_json["project"].get("name") or "Unnamed Project",
                        }
                    else:
                        project_obj = {
                            "id": task_data["pid"],
                            "name": "Project unavailable",
                        }
                except Exception:
                    project_obj = {
                        "id": task_data["pid"],
                        "name": "Project unavailable",
                    }

            # === 4. Get Creator ===
            created_by = None
            if task_data.get("created_by_uid"):
                try:
                    user_resp = await client.get(
                        f"{USERS_SERVICE_URL}/internal/{task_data['created_by_uid']}"
                    )
                    if user_resp.status_code == 200:
                        user_json = user_resp.json()
                        created_by = {
                            "id": user_json.get("id"),
                            "name": user_json.get("name")
                            or (user_json.get("email") or "").split("@")[0],
                        }
                    else:
                        created_by = {
                            "id": task_data["created_by_uid"],
                            "name": "Unknown User",
                        }
                except Exception as e:
                    print(
                        f"[ERROR] User fetch failed for {task_data['created_by_uid']}: {e}"
                    )
                    created_by = {
                        "id": task_data["created_by_uid"],
                        "name": "Unavailable",
                    }

            # === 5. Get Collaborators (list of {id, name}) ===
            collaborators_info = []
            for cid in task_data.get("collaborators") or []:
                try:
                    c_resp = await client.get(f"{USERS_SERVICE_URL}/internal/{cid}")
                    if c_resp.status_code == 200:
                        c_json = c_resp.json()
                        collaborators_info.append(
                            {
                                "id": c_json.get("id"),
                                "name": c_json.get("name")
                                or (c_json.get("email") or "").split("@")[0],
                            }
                        )
                    else:
                        collaborators_info.append({"id": cid, "name": "Unknown User"})
                except Exception as e:
                    print(f"[ERROR] Collaborator fetch failed for {cid}: {e}")
                    collaborators_info.append({"id": cid, "name": "Unavailable"})

            # === 6. Get Parent Task (id + name only) ===
            parent_task = None
            if task_data.get("parentTaskId"):
                try:
                    p_resp = await client.get(
                        f"{TASK_SERVICE_URL}/tid/{task_data['parentTaskId']}"
                    )
                    if p_resp.status_code == 200:
                        p_json = p_resp.json().get("task", p_resp.json())
                        parent_task = {
                            "id": p_json.get("id", task_data["parentTaskId"]),
                            "name": p_json.get("name") or "Unnamed Task",
                        }
                    else:
                        parent_task = {
                            "id": task_data["parentTaskId"],
                            "name": "Parent task unavailable",
                        }
                except Exception:
                    parent_task = {
                        "id": task_data["parentTaskId"],
                        "name": "Parent task unavailable",
                    }

            # === 7. Combine ===
            return {
                "message": "Task retrieved successfully",
                "task": {
                    **task_data,
                    "project": project_obj,
                    "created_by": created_by,
                    "collaborators": collaborators_info,
                    "parent_task": parent_task,
                    "status": schedule_status,
                    "deadline": schedule_deadline,
                    "start": schedule_start,  # NEW
                    "is_recurring": schedule_is_recurring,  # NEW
                    "frequency": schedule_frequency,  # NEW
                    "next_occurrence": schedule_next_occurrence,  # NEW
                },
                "metadata": {
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "queried_services": {
                        "task": True,
                        "schedule": schedule_status is not None
                        or schedule_deadline is not None,
                        "project": project_obj is not None,
                        "users": True,
                        "parent_task": parent_task is not None,
                    },
                },
            }

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Failed to connect to service: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Upstream error: {e.response.text}",
            )


# Helper function to sync project members
async def sync_project_members(project_id: str, user_ids: List[str], action: str = "add"):
    """
    Simple member sync:
    - "add": Add users to project.members (merge, don't overwrite)
    - "remove": Remove users from project.members
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get current members
            resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
            if resp.status_code != 200:
                return
            
            proj = resp.json()
            current = proj.get("project", {}).get("members", [])
            
            if action == "add":
                # Add new members (union)
                updated = list(set(current + user_ids))
            else:  # remove
                # Remove specified members
                updated = [m for m in current if m not in user_ids]
            
            # Update project
            await client.put(
                f"{PROJECTS_SERVICE_URL}/pid/{project_id}",
                json={"members": updated}
            )
    except Exception as e:
        print(f"Member sync failed: {e}")

async def ensure_members_present(project_id: str, user_ids: List[str]):
    """
    Ensure each user_id in `user_ids` exists in project's members, without overwriting.
    Strategy:
      1) GET current project -> read existing members (handles nested {project:{members:[]}} too)
      2) Compute to_add (only missing IDs)
      3) Try additive POST endpoint (bulk add) if available:
           POST /pid/{project_id}/members/add  body: { "user_ids": [...] }
         If not available (404/405), fallback to merge-PUT of the *union*.
    """
    if not user_ids:
        return

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            # -- 1) Read current members
            proj_resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
            if proj_resp.status_code != 200:
                print(
                    f"[members.ensure] WARN project {project_id} fetch -> {proj_resp.status_code}"
                )
                return

            proj_json = proj_resp.json() or {}
            # Handle both { project: {..., members: [...] } } and { members: [...] }
            current_members = (
                (proj_json.get("project") or {}).get("members")
                if isinstance(proj_json.get("project"), dict)
                else proj_json.get("members")
            ) or []

            # Normalize to strings and uniquify
            existing = set(str(m) for m in current_members if isinstance(m, str))
            to_add = [
                uid for uid in (str(u) for u in user_ids) if uid and uid not in existing
            ]

            if not to_add:
                print(f"[members.ensure] nothing to add for project {project_id}")
                return

            # -- 2) Preferred: additive POST (bulk) if your Project MS supports it
            #    e.g. Flask route idea: POST /projects/<pid>/members/add  { "user_ids": [...] }
            add_url_candidates = [
                f"{PROJECTS_SERVICE_URL}/pid/{project_id}/members/add",
                f"{PROJECTS_SERVICE_URL}/projects/{project_id}/members/add",
            ]
            for add_url in add_url_candidates:
                try:
                    add_resp = await client.post(add_url, json={"user_ids": to_add})
                    if add_resp.status_code in (200, 201, 204):
                        print(f"[members.ensure] added via POST {add_url}: {to_add}")
                        return
                    if add_resp.status_code in (404, 405):
                        # try next candidate or fallback
                        continue
                    # other non-2xx: treat as failure and try fallback
                except Exception as e:
                    print(f"[members.ensure] POST {add_url} failed: {e}")

            # -- 3) Fallback: merge-PUT (send union; DO NOT drop any existing members)
            merged = list(existing.union(to_add))
            # Choose a stable update endpoint you already use
            put_url_candidates = [
                f"{PROJECTS_SERVICE_URL}/{project_id}",
            ]
            for put_url in put_url_candidates:
                try:
                    put_resp = await client.put(put_url, json={"members": merged})
                    if put_resp.status_code in (200, 204):
                        print(f"[members.ensure] merged via PUT {put_url}: +{to_add}")
                        return
                except Exception as e:
                    print(f"[members.ensure] PUT {put_url} failed: {e}")

            print(
                f"[members.ensure] WARN: could not add members for project {project_id}: {to_add}"
            )

    except Exception as e:
        print(f"[members.ensure] ERROR: {e}")


@app.post(
    "/createTask",
    summary="Create task via composite service with full workflow",
    response_description="Created task with schedule and notifications",
)
async def create_task_composite(
    task_json: Dict[str, Any] = Body(
        ...,
        examples=
            {
                "name": "Im a gorrilla",
                "pid": "26db0258-e3a3-4454-b921-f721c3f29283",
                "desc": "Deploy the application to production environment",
                "priorityLevel": 10,
                "label": "deployment",
                "created_by_uid": "fb892a63-2401-46fc-b660-bf3fe1196d4e",
                "collaborators": ["655a9260-f871-480f-abea-ded735b2170a"],
                "schedule": {
                    "status": "pending",
                    "start": "2025-10-25T09:00:00Z",
                    "deadline": "2025-10-30T17:00:00Z",
                    "is_recurring": False
                }
            },
    )
):
    """
    Composite function to create a task with full workflow:
    1) Validate ALL inputs (parentTaskId, collaborators, project ID)
    2) Validate schedule data requirements BEFORE creating task
    3) Create the task in Task MS (only after ALL validations pass)
    4) Create schedule entry in Schedule MS (if provided)
    5) ROLLBACK task if schedule creation fails
    6) Sync project members (add task owner and collaborators if not already members)
    7) Return enriched response (project & collaborators info)
    """

    def _extract_task_id_from_json(obj: Any) -> Optional[str]:
        keys = ("id", "task_id", "tid", "uuid")

        def pick(d: Dict[str, Any]) -> Optional[str]:
            for k in keys:
                v = d.get(k)
                if isinstance(v, str) and len(v) >= 8:
                    return v
            return None

        if isinstance(obj, dict):
            v = pick(obj)
            if v:
                return v
            for container in ("task", "data", "result", "item"):
                sub = obj.get(container)
                if isinstance(sub, dict):
                    v = pick(sub)
                    if v:
                        return v
        return None

    try:
        # 0) Peel off schedule if present
        schedule_data = task_json.pop("schedule", None)

        # ===================================================================
        # STEP 1: COMPLETE ALL VALIDATIONS BEFORE ANY CREATION OPERATIONS
        # ===================================================================
        validation_results = {
            "parentTaskId": False,
            "collaborators": False,
            "project": False,
            "schedule_data": False,
        }

        # Validate parent task ID
        if task_json.get("parentTaskId"):
            await validate_parent_task_id(task_json["parentTaskId"])
            validation_results["parentTaskId"] = True

        # Validate collaborators
        if task_json.get("collaborators"):
            await validate_collaborators(task_json["collaborators"])
            validation_results["collaborators"] = True

        # Validate project ID
        if task_json.get("pid"):
            await validate_project_id(task_json["pid"])
            validation_results["project"] = True

        # Validate schedule data (if provided)
        if schedule_data:
            # Check required fields for schedule
            if not schedule_data.get("deadline"):
                raise HTTPException(
                    status_code=400, detail="Schedule requires 'deadline' field"
                )

            # Add required fields that might be missing
            if "is_recurring" not in schedule_data:
                schedule_data["is_recurring"] = False

            validation_results["schedule_data"] = True

        # ===================================================================
        # STEP 2: CREATE TASK (only after all validations pass)
        # ===================================================================
        task_id = None  # Initialize for potential rollback

        try:
            task_response = await create_task_service(task_json)
        except HTTPException as e:
            # Directly bubble up atomic service errors (e.g., "Task name already exist")
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            # General fallback for network or internal issues
            raise HTTPException(
                status_code=502,
                detail={"service": "task", "message": f"Task service failed: {str(e)}"},
            )

        # Handle downstream error bodies (e.g., {"detail": "Task name already exist"})
        if isinstance(task_response, dict) and "detail" in task_response:
            raise HTTPException(
                status_code=400,
                detail={"service": "task", "message": task_response["detail"]},
            )

        # Extract ID
        task_id = _extract_task_id_from_json(task_response)
        if not task_id:
            raise HTTPException(
                status_code=502,
                detail={
                    "service": "task",
                    "message": "Task created but no ID returned (no id/task_id/tid/uuid found in response body).",
                    "task_service_body": task_response,
                },
            )

        # ===================================================================
        # STEP 3: CREATE SCHEDULE (CRITICAL - ROLLBACK ON FAILURE)
        # ===================================================================
        schedule_response = None
        if schedule_data:
            try:
                schedule_response = await create_schedule_service(
                    task_id, schedule_data
                )

                # Check if schedule creation actually failed
                if (
                    isinstance(schedule_response, dict)
                    and schedule_response.get("status") == "failed"
                ):
                    # ROLLBACK: Delete the task that was just created
                    try:
                        await delete_task_service(task_id)
                    except Exception as rollback_error:
                        print(
                            f"CRITICAL: Failed to rollback task {task_id}: {rollback_error}"
                        )

                    # Raise error with schedule failure details
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "service": "schedule",
                            "message": "Schedule creation failed. Task creation rolled back.",
                            "error": schedule_response.get("error"),
                            "task_id_rolled_back": task_id,
                        },
                    )

            except HTTPException:
                # Re-raise HTTPException (including rollback errors from above)
                raise
            except Exception as e:
                # ROLLBACK: Delete the task that was just created
                try:
                    await delete_task_service(task_id)
                except Exception as rollback_error:
                    print(
                        f"CRITICAL: Failed to rollback task {task_id}: {rollback_error}"
                    )

                raise HTTPException(
                    status_code=502,
                    detail={
                        "service": "schedule",
                        "message": f"Schedule service failed. Task creation rolled back.",
                        "error": str(e),
                        "task_id_rolled_back": task_id,
                    },
                )

            # ===================================================================
            # STEP 4: SYNC PROJECT MEMBERS (Add task owner and collaborators)
            # ===================================================================
            project_id = task_json.get("pid")
            members_synced = {"added": []}

            if project_id:
                print(f"[MEMBERS_SYNC] Starting member sync for project {project_id}")
                try:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        # Get current project members
                        print(f"[MEMBERS_SYNC] Fetching project from: {PROJECTS_SERVICE_URL}/pid/{project_id}")
                        proj_resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
                        print(f"[MEMBERS_SYNC] GET response status: {proj_resp.status_code}")
                        
                        if proj_resp.status_code == 200:
                            proj_data = proj_resp.json()
                            print(f"[MEMBERS_SYNC] Full GET response: {proj_data}")
                            
                            # ⭐ FIX: Extract members from project field (data is None)
                            current_members = []
                            
                            # Check project field first (this is where members are!)
                            if proj_data.get("project") and isinstance(proj_data.get("project"), dict):
                                current_members = proj_data["project"].get("members", [])
                            
                            # Fallback to data if it exists
                            elif proj_data.get("data") and isinstance(proj_data.get("data"), dict):
                                current_members = proj_data["data"].get("members", [])
                            
                            # Fallback to root
                            else:
                                current_members = proj_data.get("members", [])
                            
                            # Ensure it's a list
                            if not isinstance(current_members, list):
                                current_members = []
                            
                            print(f"[MEMBERS_SYNC] Current members in DB: {current_members}")
                            
                            # Collect users to check (owner + collaborators)
                            users_to_check = []
                            
                            created_by_uid = task_json.get("created_by_uid")
                            if created_by_uid:
                                users_to_check.append(created_by_uid)
                            
                            collaborators = task_json.get("collaborators") or []
                            if isinstance(collaborators, list):
                                users_to_check.extend([c for c in collaborators if c])
                            
                            print(f"[MEMBERS_SYNC] Users to check: {users_to_check}")
                            
                            # Find users NOT in current members
                            to_add = [uid for uid in users_to_check if uid not in current_members]
                            print(f"[MEMBERS_SYNC] Users to ADD (not already in members): {to_add}")
                            
                            if to_add:
                                # MERGE: old members + new members (preserve existing)
                                updated_members = current_members + to_add
                                print(f"[MEMBERS_SYNC] Merged members array: {updated_members}")
                                
                                # Send ONLY members field
                                update_payload = {"members": updated_members}
                                
                                print(f"[MEMBERS_SYNC] Sending PUT to: {PROJECTS_SERVICE_URL}/{project_id}")
                                print(f"[MEMBERS_SYNC] Payload: {update_payload}")
                                
                                update_resp = await client.put(
                                    f"{PROJECTS_SERVICE_URL}/{project_id}",
                                    json=update_payload,
                                    headers={"Content-Type": "application/json"}
                                )
                                
                                print(f"[MEMBERS_SYNC] PUT response status: {update_resp.status_code}")
                                print(f"[MEMBERS_SYNC] PUT response body: {update_resp.text}")
                                
                                if update_resp.status_code in [200, 204]:
                                    print(f"[MEMBERS_SYNC] ✅ PUT request successful")
                                    
                                    # VERIFY: Re-fetch to check if DB actually updated
                                    print(f"[MEMBERS_SYNC] Verifying database update with fresh GET...")
                                    verify_resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
                                    
                                    if verify_resp.status_code == 200:
                                        verify_data = verify_resp.json()
                                        print(f"[MEMBERS_SYNC] 🔍 Full verify response: {verify_data}")
                                        
                                        # Extract members from project field
                                        verify_members = []
                                        
                                        if verify_data.get("project") and isinstance(verify_data.get("project"), dict):
                                            verify_members = verify_data["project"].get("members", [])
                                        elif verify_data.get("data") and isinstance(verify_data.get("data"), dict):
                                            verify_members = verify_data["data"].get("members", [])
                                        else:
                                            verify_members = verify_data.get("members", [])
                                        
                                        if not isinstance(verify_members, list):
                                            verify_members = []
                                        
                                        print(f"[MEMBERS_SYNC] 🔍 Members in DB after PUT: {verify_members}")
                                        print(f"[MEMBERS_SYNC] 🔍 Expected members: {updated_members}")
                                        
                                        # Check if all expected members are present
                                        if set(verify_members) == set(updated_members):
                                            members_synced["added"] = to_add
                                            print(f"[MEMBERS_SYNC] ✅ DATABASE VERIFIED: All members present")
                                            
                                            # ===================================================================
                                            # STEP 4.5: NOTIFY NEWLY ADDED PROJECT MEMBERS
                                            # ===================================================================
                                            if to_add:
                                                print(f"[MEMBERS_SYNC] 📧 Notifying {len(to_add)} newly added project members...")
                                                try:
                                                    # Get project name for notification
                                                    project_name = "Unknown Project"
                                                    if proj_data.get("project") and isinstance(proj_data.get("project"), dict):
                                                        project_name = proj_data["project"].get("name", "Unknown Project")
                                                    elif proj_data.get("data") and isinstance(proj_data.get("data"), dict):
                                                        project_name = proj_data["data"].get("name", "Unknown Project")
                                                    else:
                                                        project_name = proj_data.get("name", "Unknown Project")
                                                    
                                                    # Notify newly added members
                                                    notification_success = await notify_project_members_added(
                                                        project_id=project_id,
                                                        project_name=project_name,
                                                        added_member_ids=to_add,
                                                        task_name=task_json.get("name", "Unknown Task"),
                                                        added_by_user_id=task_json.get("created_by_uid")
                                                    )
                                                    
                                                    if notification_success:
                                                        print(f"[MEMBERS_SYNC] ✅ Project member notifications sent successfully")
                                                    else:
                                                        print(f"[MEMBERS_SYNC] ⚠️ Some project member notifications failed")
                                                        
                                                except Exception as e:
                                                    print(f"[MEMBERS_SYNC] ❌ Error sending project member notifications: {str(e)}")
                                                    import traceback
                                                    traceback.print_exc()
                                        else:
                                            print(f"[MEMBERS_SYNC] ⚠️ DATABASE MISMATCH!")
                                            print(f"[MEMBERS_SYNC] ⚠️ Missing: {set(updated_members) - set(verify_members)}")
                                            print(f"[MEMBERS_SYNC] ⚠️ Extra: {set(verify_members) - set(updated_members)}")
                                    else:
                                        print(f"[MEMBERS_SYNC] ⚠️ Could not verify (GET failed with {verify_resp.status_code})")
                                else:
                                    print(f"[MEMBERS_SYNC] ❌ PUT failed with status: {update_resp.status_code}")
                            else:
                                print(f"[MEMBERS_SYNC] ✅ All users already in members, skipping update")
                        else:
                            print(f"[MEMBERS_SYNC] ❌ Failed to GET project: {proj_resp.status_code}")
                                
                except Exception as e:
                    print(f"[MEMBERS_SYNC] ❌ Exception: {type(e).__name__}: {str(e)}")
                    import traceback
                    traceback.print_exc()

            # ===================================================================
            # STEP 5: ENRICH RESPONSE WITH ADDITIONAL DATA
            # ===================================================================
            project_info = None
            collaborator_info = []

            if project_id:
                try:
                    async with httpx.AsyncClient() as client:
                        proj_resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
                        if proj_resp.status_code == 200:
                            project_info = proj_resp.json()
                except Exception as e:
                    print(f"Warning: Failed to fetch project info: {e}")

            if task_json.get("collaborators"):
                try:
                    async with httpx.AsyncClient() as client:
                        for collab_id in task_json["collaborators"]:
                            user_resp = await client.get(
                                f"{USERS_SERVICE_URL}/internal/{collab_id}",
                                headers={"X-Internal-API-Key": INTERNAL_API_KEY}
                            )
                            if user_resp.status_code == 200:
                                user_data = user_resp.json()
                                collaborator_info.append({
                                    "id": user_data.get("id"),
                                    "name": user_data.get("name") or user_data.get("email", "").split("@")[0]
                                })
                except Exception as e:
                    print(f"Warning: Failed to fetch collaborator info: {e}")

        # ===================================================================
        # STEP 6: NOTIFY TASK PARTICIPANTS VIA KAFKA
        # ===================================================================
        notification_success = False
        try:
            logger.info(f"Notifying participants about new task {task_id}")
            notification_success = await notify_task_participants(task_id, task_json)
            if notification_success:
                logger.info(f"Successfully notified participants about task {task_id}")
            else:
                logger.warning(f"Failed to notify participants about task {task_id}")
        except Exception as e:
            logger.error(f"Error notifying participants about task {task_id}: {str(e)}")

        # ===================================================================
        # STEP 7: COMPOSE FINAL RESPONSE
        # ===================================================================
        return {
            "message": "Task created successfully via composite service",
            "task_id": task_id,
            "task": task_response,
            "schedule": schedule_response,
            "project_info": project_info,
            "collaborator_info": collaborator_info,
            "members_synced": members_synced,  # List of users added to project
            "notification_sent": notification_success,  # Kafka notification status
            "validations_passed": validation_results,
            "services_used": {
                "task_service": True,
                "schedule_service": schedule_response is not None,
                "project_service": project_info is not None,
                "users_service": len(collaborator_info) > 0,
                "kafka_notification": notification_success,
            },
            "created_at": datetime.now(UTC_PLUS_8).isoformat(),
        }

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Helper function to create schedule entries
async def create_schedule_service(task_id: str, schedule_data: Dict[str, Any]):
    """Create a schedule entry for the newly created task"""
    async with httpx.AsyncClient() as client:
        try:
            # Start with all schedule data fields
            schedule_payload = {
                "tid": task_id,
                **schedule_data,  # Spread all fields from schedule_data
            }

            # Add defaults for required fields if missing
            if "is_recurring" not in schedule_payload:
                schedule_payload["is_recurring"] = False
            if "status" not in schedule_payload:
                schedule_payload["status"] = "ongoing"

            response = await client.post(
                f"{SCHEDULE_SERVICE_URL}/", json=schedule_payload
            )
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "message": f"Schedule created for task {task_id}",
                    "data": response.json(),
                }
            else:
                print(
                    f"Warning: Schedule creation failed with status {response.status_code}: {response.text}"
                )
                return {
                    "status": "failed",
                    "message": f"Schedule service returned {response.status_code}",
                    "error": response.text,
                }
        except httpx.RequestError as e:
            print(f"Warning: Failed to connect to schedule service: {str(e)}")
            raise Exception(f"Schedule service unavailable: {str(e)}")


# Helper function to delete a task (for rollback)
async def delete_task_service(task_id: str):
    """Delete a task - used for rollback when schedule creation fails"""
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{TASK_SERVICE_URL}/{task_id}")
        if response.status_code not in [200, 204]:
            raise Exception(f"Failed to delete task {task_id}: {response.text}")
        return response.json() if response.status_code == 200 else None


@app.put(
    "/{task_id}",
    summary="Update task via composite service",
    response_description="Updated task with validation",
)

async def update_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)"),
    updates: Dict[str, Any] = Body(
        ...,
        examples={
            "example": {
                "name": "Update task from composite service",
                "parentTaskId": "33949f99-20d0-423d-9b26-f09292b2e40d",
            "collaborators": [
                "655a9260-f871-480f-abea-ded735b2170a",
                "d568296e-3644-4ac0-9714-dcaa0aaa5fb0",
            ],
            "pid": "695d5107-0229-481a-9301-7c0562ea52d1",
            "desc": "Set up the initial project structure and dependencies",
            "notes": "Remember to update the README file",
            "status": "in_progress",
            "deadline": "2024-12-31T23:59:59Z",
            "priorityLevel": 2,
            "label": "SetupUpdated",
            "created_by_uid": "655a9260-f871-480f-abea-ded735b2170a",
        },
}
    ),
):
    """
    Composite function to update a task with comprehensive validation:
    1. Validates and filters payload fields
    2. Validates ALL inputs (parentTaskId, collaborators, project ID, created_by_uid)
    3. Updates task via task service (only after all validations pass)
    4. Updates schedule service (status, deadline)
    5. Syncs project members (adds new collaborators, removes users no longer involved)
    """

    # ===================================================================
    # STEP 0: GET CURRENT TASK DATA TO TRACK CHANGES
    # ===================================================================
    print(f"[DEBUG] Received updates for task {task_id}:")
    print(f"[DEBUG] Raw payload: {updates}")
    try:
        async with httpx.AsyncClient() as client:
            current_task_resp = await client.get(f"{TASK_SERVICE_URL}/tid/{task_id}")
            if current_task_resp.status_code != 200:
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            current_task = current_task_resp.json().get("task", {})
            old_collaborators = set(current_task.get("collaborators") or [])
            old_owner = current_task.get("created_by_uid")
            project_id = current_task.get("pid")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch current task: {str(e)}"
        )

    # ===================================================================
    # STEP 1: VALIDATE AND FILTER PAYLOAD
    # ===================================================================
    allowed_fields = {
        "name",
        "parentTaskId",
        "collaborators",
        "pid",
        "desc",
        "notes",
        "priorityLevel",
        "label",
        "created_by_uid",
    }
    schedule_fields = {"status", "deadline", "start", "is_recurring", "frequency", "next_occurrence"}

    # Filter task updates
    filtered_updates = {}
    schedule_updates = {}

    for key, value in updates.items():
        if key in allowed_fields:
            filtered_updates[key] = value
        elif key in schedule_fields:
            schedule_updates[key] = value

    print(f"[DEBUG] Filtered task updates: {filtered_updates}")
    print(f"[DEBUG] Filtered schedule updates: {schedule_updates}")

    try:
        # ===================================================================
        # STEP 2: COMPLETE ALL VALIDATIONS BEFORE ANY UPDATE OPERATIONS
        # ===================================================================
        validation_results = {
            "parentTaskId": False,
            "collaborators": False,
            "project": False,
            "created_by_uid": False,
        }

        # Validate parent task ID
        if "parentTaskId" in filtered_updates and filtered_updates["parentTaskId"]:
            await validate_parent_task_id(filtered_updates["parentTaskId"])
            validation_results["parentTaskId"] = True

        # Validate collaborators exist in Users DB
        if "collaborators" in filtered_updates and filtered_updates["collaborators"]:
            await validate_collaborators(filtered_updates["collaborators"])
            validation_results["collaborators"] = True

        # Validate project ID exists
        if "pid" in filtered_updates and filtered_updates["pid"]:
            await validate_project_id(filtered_updates["pid"])
            validation_results["project"] = True

        # Validate created_by_uid exists in Users DB
        if "created_by_uid" in filtered_updates and filtered_updates["created_by_uid"]:
            await validate_user_exists(filtered_updates["created_by_uid"])
            validation_results["created_by_uid"] = True

        # ===================================================================
        # STEP 3: UPDATE TASK (only after all validations pass)
        # ===================================================================
        task_response = None
        if filtered_updates:
            task_response = await update_task_service(task_id, filtered_updates)

        # ===================================================================
        # STEP 4: UPDATE SCHEDULE (only after task update succeeds)
        # ===================================================================
        schedule_response = None
        if schedule_updates:
            schedule_response = await update_schedule_service(task_id, schedule_updates)

      # ===================================================================
        # STEP 5: SYNC PROJECT MEMBERS (Handle collaborator additions and removals)
        # ===================================================================
        members_synced = {"added": [], "removed": [], "skipped": []}
        
        # Only process if collaborators field was updated
        if "collaborators" in filtered_updates:
            new_collaborators = set(filtered_updates.get("collaborators", []))
            added_collaborators = new_collaborators - old_collaborators
            removed_collaborators = old_collaborators - new_collaborators
            
            if project_id and (added_collaborators or removed_collaborators):
                try:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        # Get current project members
                        proj_resp = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
                        
                        if proj_resp.status_code == 200:
                            proj_data = proj_resp.json()
                            
                            # Extract members from project field
                            current_members = []
                            if proj_data.get("project") and isinstance(proj_data.get("project"), dict):
                                current_members = proj_data["project"].get("members", [])
                            elif proj_data.get("data") and isinstance(proj_data.get("data"), dict):
                                current_members = proj_data["data"].get("members", [])
                            else:
                                current_members = proj_data.get("members", [])
                            
                            if not isinstance(current_members, list):
                                current_members = []
                            
                            print(f"[MEMBERS_SYNC] Current members: {current_members}")
                            print(f"[MEMBERS_SYNC] Added collaborators: {added_collaborators}")
                            print(f"[MEMBERS_SYNC] Removed collaborators: {removed_collaborators}")
                            
                            # --- HANDLE ADDITIONS ---
                            # Check if added collaborators already exist in members, if not, append
                            to_add = [uid for uid in added_collaborators if uid not in current_members]
                            
                            if to_add:
                                members_synced["added"] = to_add
                                print(f"[MEMBERS_SYNC] Adding new members: {to_add}")
                            else:
                                members_synced["skipped"] = list(added_collaborators)
                                print(f"[MEMBERS_SYNC] All added collaborators already in members, skipping")
                            
                            # --- HANDLE REMOVALS ---
                            # For each removed collaborator, call /tasks/user/{user_id}
                            # If results = 0, remove from members, else keep
                            to_remove = []
                            for uid in removed_collaborators:
                                try:
                                    # Check if user has any other tasks in this project
                                    tasks_resp = await client.get(f"http://manage-task:4000/tasks/user/{uid}")
                                    
                                    if tasks_resp.status_code == 200:
                                        tasks_data = tasks_resp.json()
                                        
                                        # Filter tasks for this specific project
                                        user_tasks_in_project = [
                                            task for task in tasks_data.get("tasks", [])
                                            if task.get("task", {}).get("pid") == project_id
                                        ]
                                        
                                        if len(user_tasks_in_project) == 0:
                                            # User has no other tasks in this project, safe to remove
                                            to_remove.append(uid)
                                            print(f"[MEMBERS_SYNC] User {uid} has no other tasks in project, will remove")
                                        else:
                                            print(f"[MEMBERS_SYNC] User {uid} still has {len(user_tasks_in_project)} task(s) in project, keeping in members")
                                except Exception as e:
                                    print(f"[MEMBERS_SYNC] Error checking tasks for user {uid}: {e}")
                            
                            if to_remove:
                                members_synced["removed"] = to_remove
                                print(f"[MEMBERS_SYNC] Removing members: {to_remove}")
                            
                            # --- UPDATE PROJECT MEMBERS ---
                            if to_add or to_remove:
                                # Calculate final members list
                                updated_members = [m for m in current_members if m not in to_remove]
                                updated_members.extend(to_add)
                                
                                print(f"[MEMBERS_SYNC] Final members list: {updated_members}")
                                
                                # Send update
                                update_payload = {"members": updated_members}
                                update_resp = await client.put(
                                    f"{PROJECTS_SERVICE_URL}/{project_id}",
                                    json=update_payload,
                                    headers={"Content-Type": "application/json"}
                                )
                                
                                if update_resp.status_code in [200, 204]:
                                    print(f"[MEMBERS_SYNC] ✅ Members updated successfully")
                                else:
                                    print(f"[MEMBERS_SYNC] ❌ Update failed: {update_resp.status_code}")
                        
                except Exception as e:
                    print(f"[MEMBERS_SYNC] ❌ Exception during member sync: {e}")
                    import traceback
                    traceback.print_exc()

        # ===================================================================
        # STEP 6: COMPOSE RESPONSE
        # ===================================================================
        response_data = {
            "message": "Task updated successfully via composite service",
            "task_id": task_id,
            "validations_passed": validation_results,
            "updates_applied": {
                "task_fields": list(filtered_updates.keys()),
                "schedule_fields": list(schedule_updates.keys()),
            },
            "updated_data": {},
        }

        # Merge task fields into updated_data
        if task_response:
            response_data["updated_data"].update(task_response)

        # Merge schedule fields (status, deadline) into updated_data
        if schedule_response:
            if isinstance(schedule_response, dict):
                # Extract just status and deadline
                if "status" in schedule_response:
                    response_data["updated_data"]["status"] = schedule_response[
                        "status"
                    ]
                if "deadline" in schedule_response:
                    response_data["updated_data"]["deadline"] = schedule_response[
                        "deadline"
                    ]
            else:
                response_data["updated_data"]["schedule"] = schedule_response

        return response_data

    except ValidationError as e:
        print(f"[ERROR] Validation failed for task {task_id}: {str(e)}")  # ADD THIS
        logger.error(f"Validation failed for task {task_id}: {str(e)}")   # AND THIS
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")
    except HTTPException as e:
        print(f"[ERROR] HTTP exception for task {task_id}: {e.detail}")   # ADD THIS
        logger.error(f"HTTP exception for task {task_id}: {e.detail}")    # AND THIS
        raise e
    except Exception as e:
        print(f"[ERROR] Internal error for task {task_id}: {str(e)}")     # ADD THIS
        logger.error(f"Internal error for task {task_id}: {str(e)}")      # AND THIS
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def validate_user_exists(user_id: str):
    """
    Validates that a user exists in the Users microservice.
    Raises HTTPException if user doesn't exist.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USERS_SERVICE_URL}/internal/{user_id}")
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"User with ID {user_id} not found"
                )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"User with ID {user_id} not found"
                )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Failed to validate user: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Failed to connect to Users service: {str(e)}"
            )


async def fetch_user_details(user_id: str) -> Dict[str, Any]:
    """
    Fetch user details from the Users microservice.
    Returns a dictionary with user information or None if user not found.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USERS_SERVICE_URL}/internal/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "user_id": user_data.get("id", user_id),
                    "name": user_data.get("name") or (user_data.get("email") or "").split("@")[0],
                    "email": user_data.get("email"),
                    "role": user_data.get("role"),
                    "department": user_data.get("department"),
                    "phone": user_data.get("phone")
                }
            else:
                logger.warning(f"Failed to fetch user details for {user_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching user details for {user_id}: {str(e)}")
            return None


async def notify_project_members_added(
    project_id, 
    project_name: str, 
    added_member_ids: list, 
    task_name: str,
    added_by_user_id: str = None
) -> bool:
    """
    Notify newly added project members via Kafka events.
    """
    try:
        logger.info(f"🚀 Starting project member notification for project {project_id}")
        
        # Ensure Kafka producer is connected
        if not kafka_publisher.producer:
            logger.info("📡 Connecting to Kafka producer...")
            kafka_publisher._connect()
            if not kafka_publisher.producer:
                logger.error("❌ Failed to initialize Kafka producer")
                return False
        
        # Fetch details for the user who added the members (if provided)
        added_by_name = "System"
        if added_by_user_id:
            added_by_details = await fetch_user_details(added_by_user_id)
            if added_by_details:
                added_by_name = added_by_details.get("name", "Unknown User")
        
        success_count = 0
        
        # Send notification to each newly added member
        for member_id in added_member_ids:
            logger.info(f"📤 Sending project member notification to user {member_id}")
            
            # Fetch user details for the member
            user_details = await fetch_user_details(member_id)
            if not user_details:
                logger.warning(f"⚠️ Could not fetch details for user {member_id}, skipping notification")
                continue
            
            # Prepare event data
            event_data = {
                "project_id": project_id,
                "project_name": project_name,
                "task_name": task_name,
                "added_by_name": added_by_name,
                "uid": user_details.get("user_id"),
                "name": user_details.get("name"),
                "email": user_details.get("email"),
                "role": user_details.get("role"),
                "department": user_details.get("department"),
                "phone": user_details.get("phone"),
                "timestamp": datetime.now(UTC_PLUS_8).isoformat()
            }
            
            logger.debug(f"📋 Project member notification data: {event_data}")
            
            # Publish event
            success = kafka_publisher.publish_event(
                topic=Topics.NOTIFICATION_EVENTS,
                event_type=EventTypes.PROJECT_COLLABORATOR_ADDED,
                data=event_data,
            )
            
            if success:
                success_count += 1
                logger.info(f"✅ Successfully sent project member notification to user {member_id}")
            else:
                logger.error(f"❌ Failed to send project member notification to user {member_id}")
        
        # Final flush to ensure all messages are sent
        try:
            logger.info("🔄 Flushing remaining Kafka messages...")
            kafka_publisher.producer.flush(timeout=10)
            logger.info("✅ Kafka flush completed")
        except Exception as e:
            logger.error(f"❌ Error during Kafka flush: {e}")
        
        logger.info(f"📊 Project member notifications sent: {success_count}/{len(added_member_ids)}")
        return success_count > 0
        
    except Exception as e:
        logger.error(f"❌ Error in project member notification: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# Helper functions for validations -- for update
async def validate_parent_task_id(parent_task_id: str):
    """Validate that parentTaskId exists and is valid"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{TASK_SERVICE_URL}/tid/{parent_task_id}")
            if response.status_code == 404:
                raise ValidationError(f"Parent task with ID {parent_task_id} not found")
            elif response.status_code != 200:
                raise ValidationError(
                    f"Failed to validate parent task ID: {response.status_code}"
                )
        except httpx.RequestError as e:
            raise ValidationError(
                f"Failed to connect to task service for parent validation: {str(e)}"
            )


async def validate_collaborators(collaborator_ids: List[str]):
    """Validate that all collaborator IDs exist in Users DB"""
    async with httpx.AsyncClient() as client:
        try:
            for collaborator_id in collaborator_ids:
                response = await client.get(
                    f"{USERS_SERVICE_URL}/internal/{collaborator_id}",
                    headers={"X-Internal-API-Key": INTERNAL_API_KEY},
                )

                if response.status_code == 404:
                    raise ValidationError(
                        f"Collaborator with ID {collaborator_id} not found in Users DB"
                    )
                elif response.status_code != 200:
                    raise ValidationError(
                        f"Failed to validate collaborator {collaborator_id}: {response.status_code}"
                    )

        except httpx.RequestError as e:
            raise ValidationError(f"Failed to connect to users service: {str(e)}")


async def validate_project_id(project_id: str):
    """Validate that project ID exists"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
            if response.status_code == 404:
                raise ValidationError(f"Project with ID {project_id} not found")
            elif response.status_code != 200:
                raise ValidationError(
                    f"Failed to validate project ID: {response.status_code}"
                )
        except httpx.RequestError as e:
            raise ValidationError(f"Failed to connect to projects service: {str(e)}")


async def update_task_service(task_id: str, updates: Dict[str, Any]):
    """Send updates to the task service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{TASK_SERVICE_URL}/{task_id}", json=updates)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            elif response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Task service error: {response.text}",
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Task service unavailable: {str(e)}"
            )


# Schedule Service
async def update_schedule_service(task_id: str, schedule_updates: Dict[str, Any]):
    """Send schedule updates to the schedule service using task ID"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{SCHEDULE_SERVICE_URL}/tid/{task_id}",  # Use /tid/ endpoint
                json=schedule_updates,
            )

            if response.status_code == 404:
                print(f"Warning: No schedule found for task {task_id}")
                return {
                    "status": "not_found",
                    "message": f"No schedule found for task {task_id}",
                }
            elif response.status_code == 400:
                print(f"Warning: Bad request to schedule service: {response.text}")
                return {"status": "bad_request", "message": "Invalid schedule data"}
            elif response.status_code != 200:
                print(
                    f"Warning: Schedule service returned {response.status_code}: {response.text}"
                )
                return {
                    "status": "error",
                    "message": f"Schedule service error: {response.status_code}",
                }

            return {
                "status": "success",
                "message": f"Task {task_id} schedule updated successfully",
                "data": response.json(),
            }

        except httpx.RequestError as e:
            print(f"Warning: Failed to connect to schedule service: {str(e)}")
            return {
                "status": "service_unavailable",
                "message": "Schedule service unavailable",
            }


# User Service
# async def get_current_user_UID():
# Call the atomic services
async def create_task_service(task_json: Dict[str, Any]):
    """Send a new task to the task service"""

    # get current user UID with helper function
    # get_current_user_UID():
    # append to task_json

    # UID for testing
    # task_json["created_by_uid"] = "fb892a63-2401-46fc-b660-bf3fe1196d4e"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{TASK_SERVICE_URL}/createTask", json=task_json
            )
            response.raise_for_status()  # raise error if status != 2xx
            return response.json()
        except httpx.HTTPStatusError as e:
            # Forward Task MS error as-is
            return e.response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, detail=f"Task service unavailable: {str(e)}"
            )


# Delete task by task ID
@app.delete("/{task_id}", summary="Delete a task via composite service")
async def delete_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    """
    Workflow:
      1) GET task details (owner, collaborators, project) BEFORE deletion
      2) DELETE task itself -> TASK_SERVICE_URL/{task_id}
      3) SYNC project members (check if users should be removed)

    Notes:
      - 404 from task service is treated as already deleted (idempotent).
      - Any other non-2xx/404 becomes a 502 to the client (downstream error).
    """
    project_id = None
    task_owner = None
    collaborators = []

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            # 1) Get task details BEFORE deletion (to get project_id, owner, collaborators)
            task_url = f"{TASK_SERVICE_URL}/tasks/{task_id}"
            get_resp = await client.get(task_url)

            if get_resp.status_code == 200:
                task_data = get_resp.json().get("task", {})
                project_id = task_data.get("pid")
                task_owner = task_data.get("created_by_uid")
                collaborators = task_data.get("collaborators") or []
            elif get_resp.status_code == 404:
                # Task already deleted - treat as idempotent success
                return {
                    "message": "Task already deleted (idempotent)",
                    "task_id": task_id,
                    "task_delete": {
                        "url": task_url,
                        "status_code": 404,
                        "result": "already_deleted",
                    },
                }
            else:
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "Task service get failed",
                        "status_code": get_resp.status_code,
                        "body": _safe_json(get_resp),
                        "url": task_url,
                    },
                )

            # 2) Delete the task itself
            delete_resp = await client.delete(task_url)
            if delete_resp.status_code not in (200, 204, 404):
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "Task service delete failed",
                        "status_code": delete_resp.status_code,
                        "body": _safe_json(delete_resp),
                        "url": task_url,
                    },
                )

        # 3) Sync project members (check if users should be removed)
        if project_id:
            # Check if owner should be removed from project members
            if task_owner:
                await sync_project_members(
                    project_id, task_owner, action="check_remove"
                )

            # Check if collaborators should be removed from project members
            for collaborator_id in collaborators:
                await sync_project_members(
                    project_id, collaborator_id, action="check_remove"
                )

        return {
            "message": "Delete workflow completed and project members synced",
            "task_id": task_id,
            "task_delete": {
                "url": task_url,
                "status_code": delete_resp.status_code,
                "result": _safe_json(delete_resp),
            },
            "members_sync": {
                "project_id": project_id,
                "checked_users": (
                    [task_owner] + collaborators if task_owner else collaborators
                ),
            },
        }

    except httpx.RequestError as e:
        # Network/service unavailable errors
        raise HTTPException(
            status_code=503, detail=f"Task service unavailable: {str(e)}"
        )

    except HTTPException:
        # Re-raise the structured downstream errors above
        raise

    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def _safe_json(resp: httpx.Response):
    """
    Helper to safely parse JSON bodies; falls back to text if not JSON.
    """
    try:
        return resp.json()
    except Exception:
        # Return trimmed text to avoid overly large payloads
        txt = resp.text
        return txt if len(txt) <= 2048 else txt[:2048] + "...(truncated)"


class ValidationError(Exception):
    """Custom exception for validation errors"""

    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=4000)
