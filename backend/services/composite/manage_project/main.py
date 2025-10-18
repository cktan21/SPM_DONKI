from fastapi import FastAPI, HTTPException, Path
import httpx
import asyncio
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Composite Microservice: manage-project Service")

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
TASK_SERVICE_URL = "http://tasks:5500"
USERS_SERVICE_URL = "http://users:5100" 
PROJECTS_SERVICE_URL = "http://project:5200"
SCHEDULE_SERVICE_URL = "http://schedule:5300"

# for validating user
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Composite Manage Project Service is running 🚀", "service": "manage-project-composite"}

# Favicon handler
@app.get("/favicon.ico")
async def get_favicon():
    from fastapi.responses import Response
    return Response(status_code=204)

# Get all projects by user
@app.get("/uid/{uid}", summary="Get all projects by user via composite service", response_description="List of all projects with Tasks")
async def get_project_with_tasks(uid: str):
    """
    Composite endpoint to fetch all projects by user from Project MS.
    1. Fetch all projects by user from Project MS.
    2. Fetch all tasks by project from Task MS concurrently.
    3. Return all projects with tasks in structured format.
    """
    try:
        async with httpx.AsyncClient() as client:
            # === 1. Fetch projects ===
            response = await client.get(f"{PROJECTS_SERVICE_URL}/uid/{uid}")
            response.raise_for_status()
            pms_res = response.json()
            
            # Safe access with fallback
            project_list = pms_res.get("project", [])
            if not project_list:
                return {
                    "message": "No projects found for this user",
                    "user_id": uid,
                    "projects": [],
                }

            # === 2. Prepare project data structure ===
            projects_data = {}
            project_ids = []
            
            for project in project_list:
                pid = project.get("id")
                project_ids.append(pid)
                project["tasks"] = []
                projects_data[pid] = project
            
            # === 3. Fetch tasks concurrently for all projects ===
            if project_ids:
                # Create concurrent requests
                task_requests = []
                for pid in project_ids:
                    task_requests.append(
                        client.get(f"{TASK_SERVICE_URL}/pid/{pid}")
                    )
                
                # Execute all requests concurrently
                task_responses = await asyncio.gather(*task_requests, return_exceptions=True)
                
                # Process responses and collect all task IDs for schedule fetching
                all_task_ids = []
                for i, response in enumerate(task_responses):
                    pid = project_ids[i]
                    
                    if isinstance(response, Exception):
                        print(f"Error fetching tasks for project {pid}: {response}")
                        projects_data[pid]["tasks"] = []
                    elif response.status_code == 200:
                        task_data = response.json()
                        tasks = task_data.get("tasks", [])
                        projects_data[pid]["tasks"] = tasks
                        
                        # Collect task IDs for schedule fetching
                        for task in tasks:
                            if task.get("id"):
                                all_task_ids.append(task["id"])
                    else:
                        print(f"Failed to fetch tasks for project {pid}: {response.status_code}")
                        projects_data[pid]["tasks"] = []
                
                # === 4. Fetch schedules for all tasks concurrently ===
                if all_task_ids:
                    schedule_requests = []
                    for task_id in all_task_ids:
                        schedule_requests.append(
                            client.get(f"{SCHEDULE_SERVICE_URL}/tid/{task_id}/latest")
                        )
                    
                    # Execute all schedule requests concurrently
                    schedule_responses = await asyncio.gather(*schedule_requests, return_exceptions=True)
                    
                    # Process schedule responses and attach to tasks
                    schedule_map = {}
                    for i, response in enumerate(schedule_responses):
                        task_id = all_task_ids[i]
                        
                        if isinstance(response, Exception):
                            print(f"Error fetching schedule for task {task_id}: {response}")
                            schedule_map[task_id] = None
                        elif response.status_code == 200:
                            schedule_data = response.json()
                            schedule_map[task_id] = schedule_data.get("data")
                        else:
                            print(f"Failed to fetch schedule for task {task_id}: {response.status_code}")
                            schedule_map[task_id] = None
                    
                    # Attach schedules to tasks (flatten schedule data into task)
                    for pid in project_ids:
                        for task in projects_data[pid]["tasks"]:
                            task_id = task.get("id")
                            if task_id and task_id in schedule_map:
                                schedule_data = schedule_map[task_id]
                                if schedule_data:
                                    # Flatten schedule fields directly into task
                                    task.update({
                                        "deadline": schedule_data.get("deadline"),
                                        "status": schedule_data.get("status"),
                                        "is_recurring": schedule_data.get("is_recurring"),
                                        "next_occurrence": schedule_data.get("next_occurrence"),
                                        "start": schedule_data.get("start"),
                                        "sid": schedule_data.get("sid")
                                    })

            # === 5. Convert to list format ===
            projects_list = list(projects_data.values())
            
            # === 6. Return structured response ===
            return {
                "message": "Projects retrieved successfully",
                "user_id": uid,
                "projects": projects_list,
            }
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Project service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Project service unavailable: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/pid/{project_id}", summary="Get a project by its ID", response_description="Project row")
async def get_project(
    project_id: str = Path(..., description="Project ID")
):
    try:
        async with httpx.AsyncClient() as client:
            # === 1. Fetch projects ===
            response = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
            response.raise_for_status()
            pms_res = response.json()
            
            # Safe access with fallback
            project = pms_res.get("project", [])
            if not project:
                return {
                    "message": "No projects found for this user",
                    "project_id": project_id,
                    "project": None,
                }
            
            res = await client.get(f"{TASK_SERVICE_URL}/pid/{project_id}")
            res.raise_for_status()
            task_data = res.json()
            tasks = task_data.get("tasks", [])
            project["tasks"] = tasks
            
            # === 2. Fetch schedules for all tasks ===
            if tasks:
                # Collect task IDs
                task_ids = [task.get("id") for task in tasks if task.get("id")]
                
                if task_ids:
                    # Fetch schedules concurrently
                    schedule_requests = []
                    for task_id in task_ids:
                        schedule_requests.append(
                            client.get(f"{SCHEDULE_SERVICE_URL}/tid/{task_id}/latest")
                        )
                    
                    # Execute all schedule requests concurrently
                    schedule_responses = await asyncio.gather(*schedule_requests, return_exceptions=True)
                    
                    # Process schedule responses and attach to tasks (flatten schedule data)
                    for i, response in enumerate(schedule_responses):
                        task_id = task_ids[i]
                        
                        if isinstance(response, Exception):
                            print(f"Error fetching schedule for task {task_id}: {response}")
                        elif response.status_code == 200:
                            schedule_data = response.json().get("data")
                            # Find the task and flatten schedule data into it
                            for task in project["tasks"]:
                                if task.get("id") == task_id and schedule_data:
                                    # Flatten schedule fields directly into task
                                    task.update({
                                        "deadline": schedule_data.get("deadline"),
                                        "status": schedule_data.get("status"),
                                        "is_recurring": schedule_data.get("is_recurring"),
                                        "next_occurrence": schedule_data.get("next_occurrence"),
                                        "start": schedule_data.get("start"),
                                        "sid": schedule_data.get("sid")
                                    })
                                    break
                        else:
                            print(f"Failed to fetch schedule for task {task_id}: {response.status_code}")
            
            return {
                "message": "Project retrieved successfully",
                "project_id": project_id,
                "project": project
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Project service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Project service unavailable: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4100)