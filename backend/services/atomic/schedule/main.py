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
@app.get("/tid/{tid}")
def get_schedule_by_tid(tid: str):
    data = supabase.fetch_schedule_by_tid(tid)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Task {tid} not found")
    return {"message":f"Task {tid} Schedule Retrieved Successfully" ,"data": data}

# Retrieve TID Latest
@app.get("/tid/{tid}/latest")
def get_schedule_by_tid(tid: str):
    data = supabase.fetch_schedule_by_tid(tid, latest=True)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Task {tid} not found")
    return {"message":f"Task {tid} Schedule Retrieved Successfully" ,"data": data}

# Retrieve with Schedule ID
@app.get("/sid/{sid}")
def get_schedule_by_sid(sid: str):
    data = supabase.fetch_schedule_by_sid(sid)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Task Schedule {sid} not found")
    return {"message":f"Task Schedule {sid} Retrieved Successfully" ,"data": data}

# Create new Row
@app.post("/")
def insert_new_schedule(new_data: Dict[str, Any] = Body(...) ):
    tid = new_data.get("tid")
    start = new_data.get("start", None)
    deadline = new_data.get("deadline")
    is_recurring = new_data.get("is_recurring", False)
    next_occurrence = new_data.get("next_occurrence") if is_recurring else None
    status = "ongoing"
    try:
        data = supabase.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence)
        return {"message":f"Task {tid} Schedule Inserted Successfully" ,"data": data}
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# Update the row
@app.put("/{sid}")
def update_schedule(sid: str, new_data: Dict[str, Any] = Body(...)):
    try:
        data = supabase.update_schedule(sid, new_data)
        if not data:
            raise HTTPException(status_code=404, detail=f"Task Schedule {sid} not found")
        return {"message":f"Task Schedule {sid} Updated Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Row
@app.delete("/{sid}")
def delete_schedule(sid: str):
    data = supabase.delete_schedule(sid)
    if not data:
        raise HTTPException(status_code=404, detail="Task Schedule not found")
    return {"message": f"Task Schedule {sid} deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300)