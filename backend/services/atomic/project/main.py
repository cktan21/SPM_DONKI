from fastapi import FastAPI, HTTPException, Request
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

# Get project by ID
@app.get("/{project_id}")
def get_project_by_id(project_id: str):
    """
    Get a project by its ID
    Returns the project data if found, raises HTTPException if not found
    """
    try:
        response = supabase.client.table("PROJECT").select("*").eq("id", project_id).execute()
        
        if response.data and len(response.data) > 0:
            return {
                "message": "Project retrieved successfully",
                "project": response.data[0]
            }
        else:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
            
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        print(f"Error querying project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)