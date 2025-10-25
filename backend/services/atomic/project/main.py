from fastapi import FastAPI, HTTPException, Body
from typing import Any, Dict
from fastapi.params import Path
from fastapi.responses import Response
from dotenv import load_dotenv
import uvicorn

# Import MVC components
from controllers import ProjectController
from models import ProjectCreate, ProjectUpdate

load_dotenv()

app = FastAPI(title="Atomic Microservice: Project Service")
project_controller = ProjectController()

@app.get("/")
def read_root():
    return {"message": "Project Service is running 🚀😫"}

# Get all projects
@app.get("/all", summary="Get all projects", response_description="List of all projects")
def get_all_projects():
    return project_controller.get_all_projects()


# Get project by Project ID
@app.get("/pid/{project_id}")
def get_project_by_id(project_id: str):
    """
    Get a project by its ID
    Returns the project data if found, raises HTTPException if not found
    """
    return project_controller.get_project_by_id(project_id)

# Get project by Owner UID
@app.get("/uid/{user_id}")
def get_projects_by_user_id(user_id: str):
    """
    Get projects by its user id
    Returns the project data if found, raises HTTPException if not found
    """
    return project_controller.get_projects_by_user_id(user_id)
    

# Create new Row
@app.post("/")
def insert_new_project(new_data: Dict[str, Any] = Body(...) ):
    return project_controller.create_project(new_data)

# Update the row
@app.put("/{id}")
def update_project(id: str, new_data: Dict[str, Any] = Body(...)):
    return project_controller.update_project(id, new_data)

# Delete Row
@app.delete("/{id}")
def delete_project(id: str):
    return project_controller.delete_project(id)

@app.get("/logs", summary="Get all logs")
async def get_all_logs():
    logs = project_controller.get_all_logs()
    return {"message": f"{len(logs)} log(s) retrieved", "logs": logs}

@app.get("/logs/{pid}", summary="Get a log by its ID")
async def get_log(
    pid: str = Path(..., description="ID of the log to get"),
):
    log = project_controller.get_all_logs(filter_by=pid)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log retrieved successfully", "log": log}

@app.get("/department/{department}", summary="Get projects by department")
async def get_projects_by_department(department: str):
    projects = project_controller.get_projects_by_department(department)
    return {"message": f"{len(projects)} project(s) retrieved", "projects": projects}

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)