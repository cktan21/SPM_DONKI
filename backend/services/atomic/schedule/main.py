from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from recurring_processor import recurring_processor
from dotenv import load_dotenv
import uvicorn
from datetime import datetime

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
    frequency = new_data.get("frequency") if is_recurring else None
    status = "ongoing"
    try:
        data = supabase.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence, frequency)
        
        # If it's a recurring task, schedule it
        if is_recurring and next_occurrence and frequency:
            next_occurrence_dt = datetime.fromisoformat(next_occurrence.replace('Z', '+00:00'))
            recurring_processor.schedule_recurring_task(data["sid"], frequency, next_occurrence_dt)
        
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
        
        # Handle recurring task updates
        if "is_recurring" in new_data and new_data["is_recurring"]:
            frequency = new_data.get("frequency")
            next_occurrence = new_data.get("next_occurrence")
            if frequency and next_occurrence:
                next_occurrence_dt = datetime.fromisoformat(next_occurrence.replace('Z', '+00:00'))
                recurring_processor.schedule_recurring_task(sid, frequency, next_occurrence_dt)
        elif "is_recurring" in new_data and not new_data["is_recurring"]:
            # Cancel recurring task if it's being set to non-recurring
            recurring_processor.cancel_recurring_task(sid)
        
        return {"message":f"Task Schedule {sid} Updated Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete Row
@app.delete("/{sid}")
def delete_schedule(sid: str):
    # Cancel any scheduled recurring task before deleting
    recurring_processor.cancel_recurring_task(sid)
    
    data = supabase.delete_schedule(sid)
    if not data:
        raise HTTPException(status_code=404, detail="Task Schedule not found")
    return {"message": f"Task Schedule {sid} deleted successfully"}

# Get all scheduled recurring tasks
@app.get("/recurring/scheduled")
def get_scheduled_recurring_tasks():
    jobs = recurring_processor.get_scheduled_jobs()
    return {"message": f"Found {len(jobs)} scheduled recurring tasks", "jobs": jobs}

# Get all schedules (for testing existing data)
@app.get("/recurring/all")
def get_all_recurring_schedules():
    try:
        schedules = supabase.fetch_all_recurring_schedules()
        return {"message": f"Found {len(schedules)} schedules", "schedules": schedules}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Initialize recurring tasks on startup
@app.on_event("startup")
async def startup_event():
    """Initialize all existing recurring tasks on startup"""
    try:
        recurring_tasks = supabase.fetch_recurring_tasks()
        for task in recurring_tasks:
            if task.get("next_occurrence") and task.get("frequency"):
                next_occurrence_dt = datetime.fromisoformat(task["next_occurrence"].replace('Z', '+00:00'))
                recurring_processor.schedule_recurring_task(task["sid"], task["frequency"], next_occurrence_dt)
        print(f"Initialized {len(recurring_tasks)} recurring tasks on startup")
    except Exception as e:
        print(f"Error initializing recurring tasks: {str(e)}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown the recurring processor"""
    recurring_processor.shutdown()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300)