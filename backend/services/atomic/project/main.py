from fastapi import FastAPI, HTTPException, Body
from typing import Any, Dict
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Atomic Microservice: Project Service")
supabase = SupabaseClient()

@app.get("/")
def read_root():
    return {"message": "Project Service is running 🚀😫"}

# Get project by Project ID
@app.get("/pid/{project_id}")
def get_project_by_id(project_id: str):
    """
    Get a project by its ID
    Returns the project data if found, raises HTTPException if not found
    """
    try:
        data = supabase.fetch_project_by_pid(project_id)
        if data and len(data) > 0:
            return {
                "message": f"Project with Project ID {project_id} retrieved successfully",
                "project": data
            }
        else:
            raise HTTPException(status_code=404, detail=f"Project with Project ID {project_id} not found")
            
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        print(f"Error querying project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Get project by Owner UID
@app.get("/uid/{user_id}")
def get_project_by_id(user_id: str):
    """
    Get a project by its user id
    Returns the project data if found, raises HTTPException if not found
    """
    try:
        data = supabase.fetch_project_by_uid(user_id)
        if data and len(data) > 0:
            return {
                "message": f"Projects with user id {user_id} retrieved successfully",
                "project": data
            }
        else:
            raise HTTPException(status_code=404, detail=f"Project with user id {user_id} not found")
            
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        print(f"Error querying project {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

# Create new Row
@app.post("/")
def insert_new_project(new_data: Dict[str, Any] = Body(...) ):
    try:
        uid = new_data["uid"]
        name = new_data["name"]
        desc = new_data.get("desc")
        data = supabase.insert_project(uid, name, desc)
        return {"message":f"Project Inserted Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update the row
@app.put("/{id}")
def update_project(id: str, new_data: Dict[str, Any] = Body(...)):
    try:
        data = supabase.update_project(id, new_data)
        if not data:
            raise HTTPException(status_code=404, detail=f"Project {id} not found")
        return {"message":f"Project {id} Project Updated Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Row
@app.delete("/{id}")
def delete_project(id: str):
    data = supabase.delete_project(id)
    if not data:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"Project {id} deleted successfully"}



@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)