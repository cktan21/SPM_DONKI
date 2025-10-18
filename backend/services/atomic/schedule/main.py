from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Atomic Microservice: Schedule Service")
supabase = SupabaseClient()

@app.get("/")
def read_root():
    return {"message": "Schedule Service is running 🚀😌"}

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

# Retrieve TID
@app.get("/{tid}")
def get_schedule(tid: str):
    data = supabase.fetch_schedule(tid)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Task {tid} not found")
    return {"message":f"Task {tid} Schedule Retrieved Successfully" ,"data": data}

# Create new Row
@app.post("/")
def insert_new_schedule(new_data: Dict[str, Any] = Body(...) ):
    tid = new_data.get("tid")
    deadline = new_data.get("deadline")
    status = "ongoing"
    is_recurring = new_data.get("is_recurring", False)

    try:
        data = supabase.insert_schedule(tid, deadline, status)
        return {"message":f"Task {tid} Schedule Inserted Successfully" ,"data": data}
    except Exception as e:
        # Check if it's the duplicate task message
        if str(e) == "Task with this ID already exists.":
            raise HTTPException(
                status_code=400,
                detail="Task with this ID already exists."
            )
        else:
            # For any other unexpected errors
            raise HTTPException(status_code=400, detail=str(e))

# Update the row
@app.put("/{tid}")
def update_schedule(tid: str, new_data: Dict[str, Any] = Body(...)):
    try:
        data = supabase.update_schedule(tid, new_data)
        if not data:
            raise HTTPException(status_code=404, detail=f"Task {tid} not found")
        return {"message":f"Task {tid} Schedule Updated Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Row
@app.delete("/{tid}")
def delete_schedule(tid: str):
    data = supabase.delete_schedule(tid)
    if not data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {tid} deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300)