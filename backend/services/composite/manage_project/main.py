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
USERS_SERVICE_URL = "http://user:5100" 
PROJECTS_SERVICE_URL = "http://project:5200"
SCHEDULE_SERVICE_URL = "http://schedule:5300"
MANAGE_TASK_URL = "http://manage-task:4000"


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

# ==================== Get All Projects by User (Role-Based) ====================
@app.get(
    "/uid/{uid}",
    summary="Get all projects by user via composite service (role-based access)",
    response_description="List of all projects with Tasks based on user role"
)
async def get_project_with_tasks(uid: str):
    """
    Role-based project retrieval:
    1) Fetch user info including role from Users MS
    2) HR/Admin: Get ALL projects from Project MS
    3) Staff: Get owned projects + projects where user is a member
    4) Manager: Get owned projects + projects where user is a member + department projects
    5) For each final project, get raw task IDs via Task MS, then enrich each task via Manage-Task
    6) Return structured response with user info and enriched tasks
    """
    
    # ==================== Helper Function: Extract User Name ====================
    def extract_user_name(payload: dict) -> str:
        return (
            payload.get("name")
            or payload.get("data", {}).get("name")
            or payload.get("user", {}).get("name")
            or (payload.get("email") or "").split("@")[0]
            or "Unknown User"
        )

    internal_headers = {"X-Internal-API-Key": INTERNAL_API_KEY} if INTERNAL_API_KEY else None

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # ==================== STEP 1: Fetch User Info (Name, Role, Department) ====================
            print(f"\n[DEBUG] Starting project fetch for uid: {uid}")
            user_name = "Unknown User"
            user_role = "staff"  # default role
            user_dept = None
            
            try:
                print(f"[DEBUG] Fetching user info from: {USERS_SERVICE_URL}/internal/{uid}")
                r_user = await client.get(f"{USERS_SERVICE_URL}/internal/{uid}", headers=internal_headers)
                if r_user.status_code == 200:
                    user_data = r_user.json()
                    print(f"[DEBUG] User data retrieved: {user_data}")
                    
                    user_name = extract_user_name(user_data)
                    
                    # Extract role (check multiple possible locations)
                    user_role = (
                        user_data.get("role")
                        or user_data.get("data", {}).get("role")
                        or user_data.get("user", {}).get("role")
                        or "staff"
                    ).lower()
                    
                    # Extract department
                    user_dept = (
                        user_data.get("dept")
                        or user_data.get("department")
                        or user_data.get("data", {}).get("dept")
                        or user_data.get("data", {}).get("department")
                        or user_data.get("user", {}).get("dept")
                        or user_data.get("user", {}).get("department")
                    )
                    
                    print(f"[DEBUG] Extracted - Name: {user_name}, Role: {user_role}, Dept: {user_dept}")
                else:
                    print(f"[DEBUG] User fetch returned status: {r_user.status_code}")
            except Exception as e:
                print(f"[ERROR] User fetch failed for {uid}: {e}")

            projects_by_id = {}
            project_ids = set()

            # ==================== STEP 2: Role-Based Project Retrieval ====================
            
            # --- HR or Admin: Get ALL projects ---
            if user_role in ["hr", "admin"]:
                print(f"[DEBUG] User role is {user_role} - fetching ALL projects")
                try:
                    all_projects_resp = await client.get(f"{PROJECTS_SERVICE_URL}/all", headers=internal_headers)
                    all_projects_resp.raise_for_status()
                    all_projects_json = all_projects_resp.json()
                    print(f"[DEBUG] All projects response: {all_projects_json}")
                    
                    all_projects = all_projects_json.get("project", []) or all_projects_json.get("projects", []) or []
                    print(f"[DEBUG] Retrieved {len(all_projects)} total projects")
                    
                    projects_by_id = {p.get("id"): {**p, "tasks": []} for p in all_projects if p.get("id")}
                    project_ids = set(projects_by_id.keys())
                    print(f"[DEBUG] Processed {len(project_ids)} unique projects")
                    
                except Exception as e:
                    print(f"[ERROR] Failed to fetch all projects: {e}")
                    raise HTTPException(status_code=500, detail=f"Failed to fetch all projects: {str(e)}")
            
            # --- Staff or Manager: Get owned + member projects ---
            else:
                print(f"[DEBUG] User role is {user_role} - fetching owned and member projects")
                
                # Get owned projects
                try:
                    print(f"[DEBUG] Fetching owned projects from: {PROJECTS_SERVICE_URL}/uid/{uid}")
                    owned_resp = await client.get(f"{PROJECTS_SERVICE_URL}/uid/{uid}", headers=internal_headers)
                    owned_resp.raise_for_status()
                    owned_json = owned_resp.json()
                    owned_projects = owned_json.get("project", []) or []
                    print(f"[DEBUG] Retrieved {len(owned_projects)} owned projects")

                    projects_by_id = {p.get("id"): {**p, "tasks": []} for p in owned_projects if p.get("id")}
                    project_ids = set(projects_by_id.keys())
                except Exception as e:
                    print(f"[ERROR] Failed to fetch owned projects: {e}")
                    owned_projects = []
                    projects_by_id = {}
                    project_ids = set()

                # Get ALL projects to check members[] array
                print(f"[DEBUG] Fetching all projects to check members[] array")
                all_projects_for_member_check = []
                try:
                    all_resp = await client.get(f"{PROJECTS_SERVICE_URL}/all", headers=internal_headers)
                    if all_resp.status_code == 200:
                        all_json = all_resp.json()
                        all_projects_for_member_check = all_json.get("project", []) or all_json.get("projects", []) or []
                        print(f"[DEBUG] Retrieved {len(all_projects_for_member_check)} total projects for member check")
                except Exception as e:
                    print(f"[ERROR] Failed to fetch all projects for member check: {e}")

                # Filter projects where uid is in members[] array
                for proj in all_projects_for_member_check:
                    pid = proj.get("id")
                    members = proj.get("members", []) or []
                    
                    # Check if uid is in members array
                    if pid and pid not in project_ids and uid in members:
                        print(f"[DEBUG] Found user {uid} in members[] of project {pid}")
                        projects_by_id[pid] = {**proj, "tasks": []}
                        project_ids.add(pid)

                print(f"[DEBUG] After checking members[]: {len(project_ids)} total projects")

                # --- Manager: Also get projects where owner is in the same department ---
                if user_role == "manager" and user_dept:
                    print(f"[DEBUG] User is manager in dept: {user_dept} - checking for projects with owners in same dept")
                    
                    # For each project in all_projects_for_member_check, check if owner's dept matches
                    for proj in all_projects_for_member_check:
                        pid = proj.get("id")
                        owner_uid = proj.get("uid") or proj.get("user_id")
                        
                        if pid and pid not in project_ids and owner_uid:
                            # Fetch owner's department
                            try:
                                owner_resp = await client.get(f"{USERS_SERVICE_URL}/internal/{owner_uid}", headers=internal_headers)
                                if owner_resp.status_code == 200:
                                    owner_data = owner_resp.json()
                                    owner_dept = (
                                        owner_data.get("dept")
                                        or owner_data.get("department")
                                        or owner_data.get("data", {}).get("dept")
                                        or owner_data.get("data", {}).get("department")
                                        or owner_data.get("user", {}).get("dept")
                                        or owner_data.get("user", {}).get("department")
                                    )
                                    
                                    if owner_dept and owner_dept == user_dept:
                                        print(f"[DEBUG] Found project {pid} with owner in same dept: {user_dept}")
                                        projects_by_id[pid] = {**proj, "tasks": []}
                                        project_ids.add(pid)
                            except Exception as e:
                                print(f"[ERROR] Failed to fetch owner dept for project {pid}: {e}")
                    
                    print(f"[DEBUG] After checking department projects: {len(project_ids)} total projects")

            # ==================== STEP 3: Check if No Projects Found ====================
            if not projects_by_id:
                print(f"[DEBUG] No projects found for user {uid} with role {user_role}")
                return {
                    "message": "No projects found for this user",
                    "user_id": uid,
                    "user_name": user_name,
                    "user_role": user_role,
                    "user_dept": user_dept,
                    "projects": [],
                }

            # ==================== STEP 4: Fetch Raw Tasks for All Projects ====================
            print(f"[DEBUG] Fetching tasks for {len(project_ids)} projects")
            all_pids = list(project_ids)
            task_requests = [client.get(f"{TASK_SERVICE_URL}/pid/{pid}", headers=internal_headers) for pid in all_pids]
            task_responses = await asyncio.gather(*task_requests, return_exceptions=True)

            project_tasks_map: dict[str, list[dict]] = {pid: [] for pid in all_pids}
            for i, resp in enumerate(task_responses):
                pid = all_pids[i]
                if isinstance(resp, Exception):
                    print(f"[ERROR] Error fetching tasks for project {pid}: {resp}")
                    continue
                if resp.status_code == 200:
                    td = resp.json()
                    tasks = td.get("tasks", []) if isinstance(td, dict) else td
                    if isinstance(tasks, list):
                        project_tasks_map[pid] = [t for t in tasks if isinstance(t, dict) and t.get("id")]
                        print(f"[DEBUG] Project {pid}: found {len(project_tasks_map[pid])} tasks")

            # ==================== STEP 5: Enrich Tasks via Manage-Task Service ====================
            print(f"[DEBUG] Starting task enrichment via Manage-Task service")
            for pid in all_pids:
                raw_tasks = project_tasks_map.get(pid, [])
                if not raw_tasks:
                    projects_by_id[pid]["tasks"] = []
                    continue

                tids = [t["id"] for t in raw_tasks if t.get("id")]
                print(f"[DEBUG] Enriching {len(tids)} tasks for project {pid}")
                
                reqs = [client.get(f"{MANAGE_TASK_URL}/tasks/{tid}", headers=internal_headers) for tid in tids]
                results = await asyncio.gather(*reqs, return_exceptions=True)

                enriched = []
                for tid, res in zip(tids, results):
                    fallback = next((t for t in raw_tasks if t.get("id") == tid), {})
                    
                    if isinstance(res, Exception):
                        print(f"[ERROR] Manage-Task call failed for task {tid}: {res}")
                        enriched.append(fallback)
                        continue
                        
                    if getattr(res, "status_code", 0) == 200:
                        try:
                            payload = res.json()
                            task_obj = payload.get("task") if isinstance(payload, dict) else None
                            if not task_obj and isinstance(payload, dict):
                                task_obj = payload
                            if isinstance(task_obj, dict) and task_obj:
                                task_obj = {**fallback, **task_obj}
                                enriched.append(task_obj)
                                print(f"[DEBUG] Successfully enriched task {tid}")
                            else:
                                print(f"[WARN] Unexpected task shape for {tid}, using fallback")
                                enriched.append(fallback)
                        except Exception as e:
                            print(f"[ERROR] Failed parsing Manage-Task response for {tid}: {e}")
                            enriched.append(fallback)
                    else:
                        print(f"[WARN] Manage-Task returned {res.status_code} for {tid}")
                        enriched.append(fallback)

                projects_by_id[pid]["tasks"] = enriched

            # ==================== STEP 6: Return Final Response ====================
            print(f"[DEBUG] Successfully completed. Returning {len(projects_by_id)} projects for user {uid}")
            return {
                "message": "Projects retrieved successfully",
                "user_id": uid,
                "user_name": user_name,
                "user_role": user_role,
                "user_dept": user_dept,
                "projects": list(projects_by_id.values()),
            }

        except httpx.HTTPStatusError as e:
            print(f"[ERROR] HTTP Status Error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Project service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            print(f"[ERROR] Request Error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Project service unavailable: {str(e)}"
            )
        except Exception as e:
            print(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )



@app.get(
    "/pid/{project_id}",
    summary="Get a project by its ID",
    response_description="Project row with tasks (enriched via Manage-Task) and owner name"
)
async def get_project(
    project_id: str = Path(..., description="Project ID")
):
    try:
        # Header for internal routes (e.g., Users MS /internal/*, and any other internal endpoints)
        internal_headers = {"X-Internal-API-Key": INTERNAL_API_KEY} if INTERNAL_API_KEY else None

        async with httpx.AsyncClient(timeout=10.0) as client:
            # === 1) Fetch project ===
            r_project = await client.get(f"{PROJECTS_SERVICE_URL}/pid/{project_id}")
            r_project.raise_for_status()
            pms_res = r_project.json()

            project = pms_res.get("project")
            if not project:
                return {
                    "message": "No project found for this ID",
                    "project_id": project_id,
                    "project": None,
                }

            # === 2) Resolve owner name from Users MS ===
            user_name = "Unknown User"
            user_id = project.get("uid") or project.get("user_id")
            if user_id:
                try:
                    r_user = await client.get(f"{USERS_SERVICE_URL}/internal/{user_id}", headers=internal_headers)
                    r_user.raise_for_status()
                    up = r_user.json()
                    user_name = (
                        up.get("name")
                        or up.get("data", {}).get("name")
                        or up.get("user", {}).get("name")
                        or (up.get("email") or "").split("@")[0]
                        or "Unknown User"
                    )
                except Exception as e:
                    print(f"⚠️ Users MS lookup failed for {user_id}: {e}")
            project["owner_name"] = user_name

            # === 3) Fetch raw tasks for the project ===
            r_tasks = await client.get(f"{TASK_SERVICE_URL}/pid/{project_id}")
            r_tasks.raise_for_status()
            task_data = r_tasks.json()
            raw_tasks = task_data.get("tasks", []) or []

            # === 4) For each task, call Manage-Task: /tasks/{task_id} ===
            # This endpoint should return the enriched task (e.g., collaborators with names, latest schedule, etc.)
            if raw_tasks:
                task_ids = [t.get("id") for t in raw_tasks if t.get("id")]
                # Build requests
                reqs = [
                    client.get(f"{MANAGE_TASK_URL}/tasks/{tid}") for tid in task_ids
                ]
                # Run concurrently
                results = await asyncio.gather(*reqs, return_exceptions=True)

                enriched_tasks = []
                for idx, res in enumerate(results):
                    tid = task_ids[idx]
                    if isinstance(res, Exception):
                        print(f"⚠️ Manage-Task call failed for task {tid}: {res}")
                        # Fallback to original raw task if available
                        fallback = next((t for t in raw_tasks if t.get("id") == tid), None)
                        if fallback:
                            enriched_tasks.append(fallback)
                        continue

                    if res.status_code == 200:
                        try:
                            payload = res.json()
                            # Accept common shapes: { "task": { ... } } or the task dict directly
                            task_obj = payload.get("task") if isinstance(payload, dict) else None
                            if not task_obj and isinstance(payload, dict):
                                # If Manage-Task returns the task fields at top-level
                                task_obj = payload
                            
                            if task_obj:
                                # === NEW: Include schedule data in the task object ===
                                schedule_data = payload.get("schedule")
                                if schedule_data:
                                    # Extract the actual schedule details
                                    schedule_details = schedule_data.get("data", schedule_data)
                                    # Add key schedule fields directly to the task for easy access
                                    task_obj["status"] = schedule_details.get("status")
                                    task_obj["deadline"] = schedule_details.get("deadline")
                                    # Optionally, keep the full schedule object as well
                                    task_obj["schedule"] = schedule_details
                                
                                enriched_tasks.append(task_obj)
                            else:
                                # If shape unexpected, fall back
                                fallback = next((t for t in raw_tasks if t.get("id") == tid), None)
                                if fallback:
                                    enriched_tasks.append(fallback)
                        except Exception as e:
                            print(f"⚠️ Failed parsing Manage-Task response for {tid}: {e}")
                            fallback = next((t for t in raw_tasks if t.get("id") == tid), None)
                            if fallback:
                                enriched_tasks.append(fallback)
                    else:
                        print(f"⚠️ Manage-Task returned {res.status_code} for task {tid}")
                        fallback = next((t for t in raw_tasks if t.get("id") == tid), None)
                        if fallback:
                            enriched_tasks.append(fallback)

                project["tasks"] = enriched_tasks
            else:
                project["tasks"] = []

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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4100)