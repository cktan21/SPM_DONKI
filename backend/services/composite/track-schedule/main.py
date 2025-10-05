from fastapi import FastAPI, HTTPException, Path, Body
from typing import Dict, Any, List, Optional
import httpx
import asyncio
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Composite Microservice: track-schedule Service")

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



# Configuration for external services
TASK_SERVICE_URL = "http://localhost:5500"
USERS_SERVICE_URL = "http://localhost:5100"  
PROJECTS_SERVICE_URL = "http://localhost:5200"  
SCHEDULE_SERVICE_URL = "http://localhost:5300"  

# for validating user
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Composite Task Update Service is running 🚀", "service": "track-schedule-composite"}

# Favicon handler
@app.get("/favicon.ico")
async def get_favicon():
    from fastapi.responses import Response
    return Response(status_code=204)

# Composite endpoints
@app.get("/tasks", summary="Get all tasks via composite service", response_description="List of all tasks")
async def get_all_tasks_composite():
    """
    Composite endpoint to fetch all tasks from Task MS.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TASK_SERVICE_URL}/tasks")
            response.raise_for_status()
            return response.json()  # forward the Task MS response

    except httpx.HTTPStatusError as e:
        return e.response.json()  # forward Task MS error
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Task MS unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/tasks/{user_id}", summary="Get all tasks where user is a collaborator", response_description="List of tasks with enriched details where user is a collaborator")
async def get_tasks_by_user_composite(
    user_id: str = Path(..., description="User ID to fetch tasks for (where user is a collaborator)")
):
    """
    Composite endpoint to fetch all tasks where the user is a collaborator:
    1. Get all tasks from Task MS
    2. Filter tasks where user_id is in the collaborators array
    3. For each filtered task, enrich with schedule and project data
    4. Return list of enriched tasks
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get all tasks from Task MS
            print(f"Fetching tasks from: {TASK_SERVICE_URL}/tasks")
            tasks_response = await client.get(f"{TASK_SERVICE_URL}/tasks")
            tasks_response.raise_for_status()
            response_data = tasks_response.json()
            
            print(f"Received response: {response_data}")
            
            # Extract tasks array from response
            all_tasks = response_data.get("tasks", [])
            
            if not isinstance(all_tasks, list):
                raise HTTPException(status_code=500, detail="Unexpected response format from Task MS")

            print(f"Total tasks found: {len(all_tasks)}")

            # 2. Filter tasks where user_id is in collaborators
            user_tasks = []
            for task in all_tasks:
                collaborators = task.get("collaborators")
                print(f"Task {task.get('id')}: collaborators = {collaborators}")
                
                # Check if collaborators exists and user_id is in it
                if collaborators and isinstance(collaborators, list) and user_id in collaborators:
                    user_tasks.append(task)
                    print(f"✓ User {user_id} found in task {task.get('id')}")

            print(f"Total user tasks found: {len(user_tasks)}")

            if not user_tasks:
                return {
                    "user_id": user_id,
                    "tasks": [],
                    "count": 0,
                    "message": "No tasks found where user is a collaborator"
                }

            # 3. Enrich each task with schedule and project data
            enriched_tasks = []
            for task in user_tasks:
                task_id = task.get("id")
                
                # Get schedule information
                schedule_data = None
                try:
                    schedule_response = await client.get(f"{SCHEDULE_SERVICE_URL}/{task_id}")
                    if schedule_response.status_code == 200:
                        schedule_data = schedule_response.json()
                except Exception:
                    schedule_data = {"message": "No schedule found for this task"}

                # Get project information if task has a project ID
                project_data = None
                if task.get("pid"):
                    try:
                        project_response = await client.get(f"{PROJECTS_SERVICE_URL}/{task['pid']}")
                        if project_response.status_code == 200:
                            project_data = project_response.json()
                    except Exception:
                        project_data = {"message": "Project information unavailable"}

                enriched_tasks.append({
                    "task": task,
                    "schedule": schedule_data,
                    "project": project_data
                })

            # 4. Return comprehensive response
            return {
                "user_id": user_id,
                "tasks": enriched_tasks,
                "count": len(enriched_tasks),
                "metadata": {
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "total_tasks_checked": len(all_tasks)
                }
            }

        except httpx.HTTPStatusError as e:
            print(f"HTTPStatusError: {e}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Task MS returned an error: {e.response.text}"
            )
        except httpx.RequestError as e:
            print(f"RequestError: {e}")
            raise HTTPException(status_code=503, detail=f"Failed to connect to services: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")




@app.get("/tasks/{task_id}", summary="Get a task by ID via composite service", response_description="Comprehensive task information with schedule and project details")
async def get_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    """
    Composite endpoint to fetch comprehensive task information:
    1. Get task details from Task MS
    2. Get schedule information from Schedule MS
    3. Get project information (if task has pid)
    4. Get collaborator details from Users MS
    5. Return enriched task data
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get basic task information
            task_response = await client.get(f"{TASK_SERVICE_URL}/{task_id}")
            if task_response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found")
            task_response.raise_for_status()
            task_data = task_response.json()

            # 2. Get schedule information for this task
            schedule_data = None
            try:
                schedule_response = await client.get(f"{SCHEDULE_SERVICE_URL}/{task_id}")
                if schedule_response.status_code == 200:
                    schedule_data = schedule_response.json()
            except httpx.HTTPStatusError:
                # Schedule not found is okay, just means no schedule exists
                schedule_data = {"message": "No schedule found for this task"}

            # 3. Get project information if task has a project ID
            project_data = None
            if task_data.get("pid"):
                try:
                    project_response = await client.get(f"{PROJECTS_SERVICE_URL}/{task_data['pid']}")
                    if project_response.status_code == 200:
                        project_data = project_response.json()
                except httpx.HTTPStatusError:
                    project_data = {"message": "Project information unavailable"}

            # 4. Get collaborator details if task has collaborators
            collaborator_details = []
            if task_data.get("collaborators"):
                for collaborator_id in task_data["collaborators"]:
                    try:
                        collab_response = await client.get(
                            f"{USERS_SERVICE_URL}/internal/{collaborator_id}",
                            headers={"X-Internal-API-Key": INTERNAL_API_KEY}
                        )
                        if collab_response.status_code == 200:
                            collaborator_details.append(collab_response.json())
                        else:
                            collaborator_details.append({
                                "id": collaborator_id,
                                "message": "User details unavailable"
                            })
                    except httpx.HTTPStatusError:
                        collaborator_details.append({
                            "id": collaborator_id,
                            "message": "User not found"
                        })

            # 5. Compose the comprehensive response
            composite_response = {
                "task": task_data,
                "schedule": schedule_data,
                "project": project_data,
                "collaborator_details": collaborator_details,
                "metadata": {
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "services_queried": {
                        "task_service": True,
                        "schedule_service": schedule_data is not None,
                        "project_service": project_data is not None,
                        "users_service": len(collaborator_details) > 0
                    }
                }
            }

            return composite_response

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Task not found in Task MS")
            else:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"Task MS returned an error: {e.response.text}"
                )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to services: {str(e)}")

@app.post("/createTask", summary="Create task via composite service with full workflow", response_description="Created task with schedule and notifications")
async def create_task_composite(
    task_json: Dict[str, Any] = Body(
        ...,
        example={
            "name": "New Task Title",
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "parentTaskId": "1991067d-18d4-48c4-987b-7c06743725b4",
            "collaborators": [
                "0ec8a99d-3aab-4ec6-b692-fda88656844f",
                "17a40371-66fe-411a-963b-a977cc7cb475"
            ],
            "desc": "Optional description",
            "notes": "Optional notes",
            "schedule": {
                "status": "todo",
                "deadline": "2024-12-31T23:59:59Z",
                "priority": "medium"
            }
        }
    )
):
    """
    Composite function to create a task with full workflow:
    1) Validate parentTaskId, collaborators, project ID (same helpers as PUT)
    2) Create the task in Task MS
    3) Create schedule entry in Schedule MS (if provided)
    4) Return enriched response (project & collaborators info)
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

        # 1) VALIDATIONS
        if task_json.get("parentTaskId"):
            await validate_parent_task_id(task_json["parentTaskId"])

        if task_json.get("collaborators"):
            await validate_collaborators(task_json["collaborators"])

        if task_json.get("pid"):
            await validate_project_id(task_json["pid"])

        # 2) CREATE TASK
        try:
            task_response = await create_task_service(task_json)
        except HTTPException as e:
            # Directly bubble up atomic service errors (e.g., "Task name already exist")
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            # General fallback for network or internal issues
            raise HTTPException(
                status_code=502,
                detail={"service": "task", "message": f"Task service failed: {str(e)}"}
            )

        # Handle downstream error bodies (e.g., {"detail": "Task name already exist"})
        if isinstance(task_response, dict) and "detail" in task_response:
            raise HTTPException(
                status_code=400,
                detail={"service": "task", "message": task_response["detail"]}
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

        # 3) CREATE SCHEDULE (optional)
        schedule_response = None
        if schedule_data:
            try:
                schedule_response = await create_schedule_service(task_id, schedule_data)
            except Exception as e:
                raise HTTPException(
                    status_code=502,
                    detail={"service": "schedule", "message": f"Schedule service failed: {str(e)}"}
                )

        # 4) ENRICH: project info (optional)
        project_info = None
        if task_json.get("pid"):
            try:
                async with httpx.AsyncClient() as client:
                    proj_resp = await client.get(f"{PROJECTS_SERVICE_URL}/{task_json['pid']}")
                    project_info = proj_resp.json() if proj_resp.status_code == 200 else {
                        "message": f"Project details unavailable (status {proj_resp.status_code})"
                    }
            except Exception as ex:
                project_info = {"message": f"Project details unavailable: {str(ex)}"}

        # 5) ENRICH: collaborator info (optional)
        collaborator_info = []
        if task_json.get("collaborators"):
            async with httpx.AsyncClient() as client:
                for collab_id in task_json["collaborators"]:
                    try:
                        collab_resp = await client.get(
                            f"{USERS_SERVICE_URL}/internal/{collab_id}",
                            headers={"X-Internal-API-Key": INTERNAL_API_KEY} if INTERNAL_API_KEY else None,
                        )
                        if collab_resp.status_code == 200:
                            collaborator_info.append(collab_resp.json())
                        else:
                            collaborator_info.append(
                                {"id": collab_id, "message": f"Details unavailable (status {collab_resp.status_code})"}
                            )
                    except Exception as ex:
                        collaborator_info.append({"id": collab_id, "message": f"Details unavailable: {str(ex)}"})

        # 6) Compose final response
        return {
            "message": "Task created successfully via composite service",
            "task_id": task_id,
            "task": task_response,
            "schedule": schedule_response,
            "project_info": project_info,
            "collaborator_info": collaborator_info,
            "validations_passed": {
                "parentTaskId": bool(task_json.get("parentTaskId")),
                "collaborators": bool(task_json.get("collaborators")),
                "project": bool(task_json.get("pid")),
            },
            "services_used": {
                "task_service": True,
                "schedule_service": schedule_response is not None,
                "project_service": project_info is not None,
                "users_service": len(collaborator_info) > 0,
            },
            "created_at": datetime.now(timezone.utc).isoformat(),
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
            # Add task_id to schedule data
            schedule_payload = {
                "task_id": task_id,
                **schedule_data
            }
            
            response = await client.post(f"{SCHEDULE_SERVICE_URL}/schedules", json=schedule_payload)
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "message": f"Schedule created for task {task_id}",
                    "data": response.json()
                }
            else:
                print(f"Warning: Schedule creation failed with status {response.status_code}: {response.text}")
                return {
                    "status": "failed",
                    "message": f"Schedule service returned {response.status_code}",
                    "error": response.text[:200]  # Truncate error message
                }
        except httpx.RequestError as e:
            print(f"Warning: Failed to connect to schedule service: {str(e)}")
            return {
                "status": "service_unavailable",
                "message": "Schedule service unavailable"
            }
    
@app.put("/{task_id}", summary="Update task via composite service", response_description="Updated task with validation")
async def update_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)"),
    updates: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Update task from composite service",
            "parentTaskId": "b1692687-4e49-41b1-bb04-3f5c18d6faf7",
            "collaborators": ["0ec8a99d-3aab-4ec6-b692-fda88656844f", "17a40371-66fe-411a-963b-a977cc7cb475"],
            "pid": "40339da5-9a62-4195-bbe5-c69f2fc04ed6",
            "desc": "Set up the initial project structure and dependencies",
            "notes": "Remember to update the README file",
            "status": "in_progress",
            "deadline": "2024-12-31T23:59:59Z"
        }
    ),
):
    """
    Composite function to update a task with comprehensive validation:
    1. Validates payload fields
    2. Checks parentTaskId validity
    3. Verifies collaborators exist in Users DB
    4. Validates project ID exists
    5. Updates task via task service
    6. Updates schedule service (status, deadline)
    """
    
    # Step 1: Validate and filter payload
    allowed_fields = {"name", "parentTaskId", "collaborators", "pid", "desc", "notes"}
    schedule_fields = {"status", "deadline"}
    
    # Filter task updates
    filtered_updates = {}
    schedule_updates = {}
    
    for key, value in updates.items():
        if key in allowed_fields:
            filtered_updates[key] = value
        elif key in schedule_fields:
            schedule_updates[key] = value
    
    try:
        # Step 2: Check parentTaskId is valid (if provided)
        if "parentTaskId" in filtered_updates and filtered_updates["parentTaskId"]:
            await validate_parent_task_id(filtered_updates["parentTaskId"])
        
        # Step 3: Check collaborators exist in Users DB (if provided)
        if "collaborators" in filtered_updates and filtered_updates["collaborators"]:
            await validate_collaborators(filtered_updates["collaborators"])
        
        # Step 4: Check project ID exists (if provided)
        if "pid" in filtered_updates and filtered_updates["pid"]:
            await validate_project_id(filtered_updates["pid"])
        
        # Step 5: Send payload to task service (only if there are task updates)
        task_response = None
        if filtered_updates:
            task_response = await update_task_service(task_id, filtered_updates)
        
        # Step 6: Send schedule updates to schedule service (if any)
        schedule_response = None
        if schedule_updates:
            schedule_response = await update_schedule_service(task_id, schedule_updates)
        
        # Prepare response
        response_data = {
            "message": "Task updated successfully via composite service",
            "task_id": task_id,
            "validations_passed": {
                "parentTaskId": "parentTaskId" in filtered_updates,
                "collaborators": "collaborators" in filtered_updates,
                "project": "pid" in filtered_updates
            },
            "updates_applied": {
                "task_fields": list(filtered_updates.keys()),
                "schedule_fields": list(schedule_updates.keys())
            }
        }
        
        if task_response:
            response_data["task"] = task_response
        
        if schedule_response:
            response_data["schedule_updated"] = True
            response_data["schedule_info"] = schedule_response
        
        return response_data
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Helper functions for validations -- for update
async def validate_parent_task_id(parent_task_id: str):
    """Validate that parentTaskId exists and is valid"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{TASK_SERVICE_URL}/{parent_task_id}")
            if response.status_code == 404:
                raise ValidationError(f"Parent task with ID {parent_task_id} not found")
            elif response.status_code != 200:
                raise ValidationError(f"Failed to validate parent task ID: {response.status_code}")
        except httpx.RequestError as e:
            raise ValidationError(f"Failed to connect to task service for parent validation: {str(e)}")


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
            response = await client.get(f"{PROJECTS_SERVICE_URL}/{project_id}")
            if response.status_code == 404:
                raise ValidationError(f"Project with ID {project_id} not found")
            elif response.status_code != 200:
                raise ValidationError(f"Failed to validate project ID: {response.status_code}")
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
                raise HTTPException(status_code=response.status_code, detail=f"Task service error: {response.text}")
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Task service unavailable: {str(e)}")

# Schedule Service
async def update_schedule_service(task_id: str, schedule_updates: Dict[str, Any]):
    """Send schedule updates to the schedule service matching the PUT /{tid} endpoint"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{SCHEDULE_SERVICE_URL}/{task_id}", json=schedule_updates)
            
            if response.status_code == 404:
                print(f"Warning: Task {task_id} not found in schedule service")
                return {"status": "not_found", "message": f"Task {task_id} not found in schedule service"}
            elif response.status_code == 400:
                print(f"Warning: Bad request to schedule service: {response.text}")
                return {"status": "bad_request", "message": "Invalid schedule data"}
            elif response.status_code != 200:
                print(f"Warning: Schedule service returned {response.status_code}: {response.text}")
                return {"status": "error", "message": f"Schedule service error: {response.status_code}"}
            
            return {
                "status": "success",
                "message": f"Task {task_id} schedule updated successfully",
                "data": response.json()
            }
            
        except httpx.RequestError as e:
            print(f"Warning: Failed to connect to schedule service: {str(e)}")
            return {"status": "service_unavailable", "message": "Schedule service unavailable"}

#User Service
#async def get_current_user_UID():
# Call the atomic services
async def create_task_service(task_json: Dict[str, Any]):
    """Send a new task to the task service"""

    #get current user UID with helper function
    #get_current_user_UID():
    #append to task_json

    # UID for testing
    task_json["created_by_uid"] = "7b055ff5-84f4-47bc-be7d-5905caec3ec6"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{TASK_SERVICE_URL}/createTask", json=task_json)
            response.raise_for_status()  # raise error if status != 2xx
            return response.json()
        except httpx.HTTPStatusError as e:
            # Forward Task MS error as-is
            return e.response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Task service unavailable: {str(e)}")

# Delete task by task ID
@app.delete("/{task_id}", summary="Delete a task via composite service")
async def delete_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    """
    Workflow:
      1) DELETE schedules for this task -> SCHEDULE_SERVICE_URL/schedule_api/{task_id}
      2) DELETE task itself            -> TASK_SERVICE_URL/task_api/{task_id}

    Notes:
      - 404 from either service is treated as already deleted (idempotent).
      - Any other non-2xx/404 becomes a 502 to the client (downstream error).
    """
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            # 1) Delete related schedules first (safe to ignore 404s)
            sched_url = f"{SCHEDULE_SERVICE_URL}/{task_id}"
            sched_resp = await client.delete(sched_url)
            if sched_resp.status_code not in (200, 204, 404):
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "Schedule service delete failed",
                        "status_code": sched_resp.status_code,
                        "body": _safe_json(sched_resp),
                        "url": sched_url,
                    },
                )

            # 2) Delete the task itself (also treat 404 as already deleted)
            task_url = f"{TASK_SERVICE_URL}/{task_id}"
            task_resp = await client.delete(task_url)
            if task_resp.status_code not in (200, 204, 404):
                raise HTTPException(
                    status_code=502,
                    detail={
                        "message": "Task service delete failed",
                        "status_code": task_resp.status_code,
                        "body": _safe_json(task_resp),
                        "url": task_url,
                    },
                )

        return {
            "message": "Delete workflow completed",
            "task_id": task_id,
            "schedule_delete": {
                "url": sched_url,
                "status_code": sched_resp.status_code,
                "result": _safe_json(sched_resp),
            },
            "task_delete": {
                "url": task_url,
                "status_code": task_resp.status_code,
                "result": _safe_json(task_resp),
            },
        }

    except httpx.RequestError as e:
        # Network/service unavailable errors
        raise HTTPException(status_code=503, detail=f"Task service unavailable: {str(e)}")

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
    uvicorn.run(app, host="0.0.0.0", port=5600)