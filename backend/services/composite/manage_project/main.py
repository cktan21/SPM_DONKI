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


# Get all projects by user (project owner + task collaborators)
@app.get(
    "/uid/{uid}",
    summary="Get all projects by user via composite service",
    response_description="List of all projects with Tasks"
)
async def get_project_with_tasks(uid: str):
    """
    1) Fetch owned projects from Project MS.
    2) Find collaborator project IDs via Task MS and merge.
    3) For each final project, get raw task IDs via Task MS, then enrich each task by calling Manage-Task /tasks/{task_id}.
    4) Return structured response with top-level user_name and enriched tasks.
    """
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
            # === 0) Resolve top-level user's name ===
            user_name = "Unknown User"
            try:
                r_user = await client.get(f"{USERS_SERVICE_URL}/internal/{uid}", headers=internal_headers)
                if r_user.status_code == 200:
                    user_name = extract_user_name(r_user.json())
            except Exception as e:
                print(f"[Users] main user fetch error for {uid}: {e}")

            # === 1) Owned projects ===
            owned_resp = await client.get(f"{PROJECTS_SERVICE_URL}/uid/{uid}", headers=internal_headers)
            owned_resp.raise_for_status()
            owned_json = owned_resp.json()
            owned_projects = owned_json.get("project", []) or []

            projects_by_id = {p.get("id"): {**p, "tasks": []} for p in owned_projects if p.get("id")}
            project_ids = set(projects_by_id.keys())

            # === 2) Collaborator projects (via Task MS) ===
            collab_pids: set[str] = set()
            try:
                c1 = await client.get(f"{TASK_SERVICE_URL}/by-collaborator/{uid}/pids", headers=internal_headers)
                if c1.status_code == 200:
                    data = c1.json()
                    if isinstance(data, dict) and isinstance(data.get("pids"), list):
                        collab_pids.update([pid for pid in data["pids"] if pid])
                else:
                    c2 = await client.get(f"{TASK_SERVICE_URL}/by-collaborator/{uid}", headers=internal_headers)
                    if c2.status_code == 200:
                        d2 = c2.json()
                        task_list = d2.get("tasks") if isinstance(d2, dict) else d2
                        if isinstance(task_list, list):
                            for t in task_list:
                                pid = (t or {}).get("pid")
                                if pid:
                                    collab_pids.add(pid)
                    else:
                        c3 = await client.get(f"{TASK_SERVICE_URL}/search?collaborator={uid}", headers=internal_headers)
                        if c3.status_code == 200:
                            d3 = c3.json()
                            tl = d3.get("tasks") if isinstance(d3, dict) else d3
                            if isinstance(tl, list):
                                for t in tl:
                                    pid = (t or {}).get("pid")
                                    if pid:
                                        collab_pids.add(pid)
            except Exception as e:
                print(f"[Tasks] collaborator PIDs fetch error for {uid}: {e}")

            collab_pids_to_fetch = [pid for pid in collab_pids if pid and pid not in project_ids]

            # Fetch collaborator projects and merge
            if collab_pids_to_fetch:
                bulk_url = f"{PROJECTS_SERVICE_URL}/ids?in={','.join(collab_pids_to_fetch)}"
                collab_projects = []
                try:
                    bulk_resp = await client.get(bulk_url, headers=internal_headers)
                    if bulk_resp.status_code == 200:
                        bj = bulk_resp.json()
                        collab_projects = bj.get("project", []) or bj.get("projects", []) or []
                except Exception:
                    collab_projects = []

                if not collab_projects:
                    loop_results = await asyncio.gather(
                        *[client.get(f"{PROJECTS_SERVICE_URL}/pid/{pid}", headers=internal_headers) for pid in collab_pids_to_fetch],
                        return_exceptions=True
                    )
                    for i, r in enumerate(loop_results):
                        pid = collab_pids_to_fetch[i]
                        if isinstance(r, Exception):
                            print(f"[Project] collab project fetch error for pid={pid}: {r}")
                            continue
                        if r.status_code == 200:
                            pj = r.json()
                            proj_obj = pj.get("project", pj)
                            if isinstance(proj_obj, dict) and proj_obj.get("id"):
                                collab_projects.append(proj_obj)

                for p in collab_projects:
                    pid = p.get("id")
                    if pid and pid not in projects_by_id:
                        projects_by_id[pid] = {**p, "tasks": []}
                        project_ids.add(pid)

            if not projects_by_id:
                return {
                    "message": "No projects found for this user",
                    "user_id": uid,
                    "user_name": user_name,
                    "projects": [],
                }

            # === 3) Fetch raw tasks for ALL final projects (to get task IDs) ===
            all_pids = list(project_ids)
            task_requests = [client.get(f"{TASK_SERVICE_URL}/pid/{pid}", headers=internal_headers) for pid in all_pids]
            task_responses = await asyncio.gather(*task_requests, return_exceptions=True)

            project_tasks_map: dict[str, list[dict]] = {pid: [] for pid in all_pids}
            for i, resp in enumerate(task_responses):
                pid = all_pids[i]
                if isinstance(resp, Exception):
                    print(f"[Tasks] error fetching tasks for project {pid}: {resp}")
                    continue
                if resp.status_code == 200:
                    td = resp.json()
                    tasks = td.get("tasks", []) if isinstance(td, dict) else td
                    if isinstance(tasks, list):
                        project_tasks_map[pid] = [t for t in tasks if isinstance(t, dict) and t.get("id")]

            # === 4) Enrich each task via Manage-Task: /tasks/{task_id} ===
            for pid in all_pids:
                raw_tasks = project_tasks_map.get(pid, [])
                if not raw_tasks:
                    projects_by_id[pid]["tasks"] = []
                    continue

                tids = [t["id"] for t in raw_tasks if t.get("id")]
                reqs = [client.get(f"{MANAGE_TASK_URL}/tasks/{tid}", headers=internal_headers) for tid in tids]
                results = await asyncio.gather(*reqs, return_exceptions=True)

                enriched = []
                for tid, res in zip(tids, results):
                    # Fallback to the original raw task if enrichment fails
                    fallback = next((t for t in raw_tasks if t.get("id") == tid), {})
                    if isinstance(res, Exception):
                        print(f"⚠️ Manage-Task call failed for task {tid}: {res}")
                        enriched.append(fallback)
                        continue
                    if getattr(res, "status_code", 0) == 200:
                        try:
                            payload = res.json()
                            task_obj = payload.get("task") if isinstance(payload, dict) else None
                            if not task_obj and isinstance(payload, dict):
                                task_obj = payload  # support flat shape
                            if isinstance(task_obj, dict) and task_obj:
                                # optional: merge with fallback so we don't lose fields
                                task_obj = {**fallback, **task_obj}
                                enriched.append(task_obj)
                            else:
                                enriched.append(fallback)
                        except Exception as e:
                            print(f"⚠️ Failed parsing Manage-Task response for {tid}: {e}")
                            enriched.append(fallback)
                    else:
                        print(f"⚠️ Manage-Task returned {res.status_code} for {tid}")
                        enriched.append(fallback)

                projects_by_id[pid]["tasks"] = enriched

            # === 5) Return (no need to do separate schedule/user map; Manage-Task provides enrichment) ===
            return {
                "message": "Projects retrieved successfully",
                "user_id": uid,
                "user_name": user_name,
                "projects": list(projects_by_id.values()),
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Project service error: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Project service unavailable: {str(e)}"
            )
        except Exception as e:
            print(f"[Composite] unexpected error: {type(e).__name__}: {e}")
            import traceback; traceback.print_exc()
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
    
# Get all projects
@app.get(
    "/Allprojects",
    summary="Get all projects (atomic)",
    response_description="Raw list of projects from Project MS"
)
async def get_all_projects():
    """
    Atomic getAll: fetch and return all projects directly from the Project MS.
    No enrichment, no fan-out calls—just a thin pass-through.
    """
    internal_headers = {"X-Internal-API-Key": INTERNAL_API_KEY} if INTERNAL_API_KEY else None

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Keep it simple: try a primary route, then one fallback.
            r = await client.get(f"{PROJECTS_SERVICE_URL}/all", headers=internal_headers)
            if r.status_code != 200:
                r = await client.get(f"{PROJECTS_SERVICE_URL}/projects", headers=internal_headers)

            r.raise_for_status()
            data = r.json()

            # Normalize common shapes to a plain list
            if isinstance(data, list):
                projects = data
            elif isinstance(data, dict):
                projects = data.get("projects") or data.get("project") or data.get("data") or []
            else:
                projects = []

            return {
                "message": "Projects retrieved",
                "count": len(projects),
                "projects": projects,
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Project service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4100)