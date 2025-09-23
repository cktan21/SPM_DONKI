from fastapi import FastAPI, HTTPException, Path, Body
from typing import Dict, Any, List, Optional
import httpx
import asyncio
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Composite Microservice: track-schedule Service")


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


# Helper functions for validations 
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


# Call the atomic services
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


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5400)