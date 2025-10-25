from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn
import httpx
import logging
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Atomic Microservice: Schedule Service")
supabase = SupabaseClient()

# Notify User Service URL
NOTIFY_USER_SERVICE_URL = "http://notify_user:4500"

async def notify_schedule_added(schedule_data: Dict[str, Any]):
    """Notify the notify_user service when a new recurring task is added"""
    import asyncio
    
    # Try multiple connection methods with retries
    urls_to_try = [
        NOTIFY_USER_SERVICE_URL,  # Original hostname
        "http://172.18.0.10:4500",  # Direct IP address
        "http://notify-user:4500",  # Alternative hostname format
    ]
    
    for attempt in range(3):  # 3 attempts
        for url in urls_to_try:
            try:
                async with httpx.AsyncClient() as client:
                    logger.info(f"Attempting to notify notify_user service at {url} (attempt {attempt + 1})")
                    response = await client.post(
                        f"{url}/schedule/update",
                        json=schedule_data,
                        timeout=10.0
                    )
                    if response.status_code == 200:
                        logger.info(f"Successfully notified notify_user service about new recurring task {schedule_data.get('sid')}")
                        return  # Success, exit function
                    else:
                        logger.warning(f"Failed to notify notify_user service at {url}: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error connecting to {url}: {str(e)}")
                continue
        
        # Wait before retry
        if attempt < 2:  # Don't wait after the last attempt
            await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
    
    # If all attempts failed, log the error but don't crash the main operation
    logger.error(f"Failed to notify notify_user service after all attempts for task {schedule_data.get('sid')}")

async def notify_deadline_monitoring_added(deadline_data: Dict[str, Any]):
    """Notify the notify_user service when deadline monitoring should be set up"""
    import asyncio
    
    # Try multiple connection methods with retries
    urls_to_try = [
        NOTIFY_USER_SERVICE_URL,  # Original hostname
        "http://172.18.0.10:4500",  # Direct IP address
        "http://notify-user:4500",  # Alternative hostname format
    ]
    
    for attempt in range(3):  # 3 attempts
        for url in urls_to_try:
            try:
                async with httpx.AsyncClient() as client:
                    logger.info(f"Attempting to notify notify_user service about deadline monitoring at {url} (attempt {attempt + 1})")
                    response = await client.post(
                        f"{url}/task/deadline/schedule",
                        json=deadline_data,
                        timeout=10.0
                    )
                    if response.status_code == 200:
                        logger.info(f"Successfully notified notify_user service about deadline monitoring for task {deadline_data.get('sid')}")
                        return  # Success, exit function
                    else:
                        logger.warning(f"Failed to notify notify_user service at {url}: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error connecting to {url}: {str(e)}")
                continue
        
        # Wait before retry
        if attempt < 2:  # Don't wait after the last attempt
            await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
    
    # If all attempts failed, log the error but don't crash the main operation
    logger.error(f"Failed to notify notify_user service about deadline monitoring after all attempts for task {deadline_data.get('sid')}")

async def notify_recurring_task_updated(schedule_data: Dict[str, Any]):
    """Notify the notify_user service when a recurring task is updated"""
    import asyncio
    
    # Try multiple connection methods with retries
    urls_to_try = [
        NOTIFY_USER_SERVICE_URL,  # Original hostname
        "http://172.18.0.10:4500",  # Direct IP address
        "http://notify-user:4500",  # Alternative hostname format
    ]
    
    for attempt in range(3):  # 3 attempts
        for url in urls_to_try:
            try:
                async with httpx.AsyncClient() as client:
                    logger.info(f"Attempting to notify notify_user service of update at {url} (attempt {attempt + 1})")
                    response = await client.post(
                        f"{url}/task/recurring/update",
                        json=schedule_data,
                        timeout=10.0
                    )
                    if response.status_code == 200:
                        logger.info(f"Successfully notified notify_user service about updated recurring task {schedule_data.get('sid')}")
                        return  # Success, exit function
                    else:
                        logger.warning(f"Failed to notify notify_user service at {url}: {response.status_code}")
            except Exception as e:
                logger.warning(f"Error connecting to {url}: {str(e)}")
                continue
        
        # Wait before retry
        if attempt < 2:  # Don't wait after the last attempt
            await asyncio.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
    
    # If all attempts failed, log the error but don't crash the main operation
    logger.error(f"Failed to notify notify_user service after all attempts for task {schedule_data.get('sid')}")

def has_cron_affecting_changes(old_data: Dict[str, Any], new_data: Dict[str, Any]) -> bool:
    """Check if any fields that affect cron jobs have changed"""
    cron_affecting_fields = ['is_recurring', 'frequency', 'next_occurrence', 'start', 'deadline']
    
    for field in cron_affecting_fields:
        if field in new_data and old_data.get(field) != new_data.get(field):
            logger.info(f"Detected change in cron-affecting field '{field}': {old_data.get(field)} -> {new_data.get(field)}")
            return True
    
    return False

@app.get("/health")
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

@app.get("/all")
def get_all_schedules():
    data = supabase.fetch_all_schedules()
    return {"message":f"All Schedules Retrieved Successfully" ,"data": data}

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
async def insert_new_schedule(new_data: Dict[str, Any] = Body(...) ):
    print(new_data)
    tid = new_data.get("tid")
    start = new_data.get("start", None)
    deadline = new_data.get("deadline")
    is_recurring = new_data.get("is_recurring", False)
    next_occurrence = new_data.get("next_occurrence") if is_recurring else None
    frequency = new_data.get("frequency") if is_recurring else None
    status = new_data.get("status")
    is_recurring = new_data.get("is_recurring", False)

    try:
        data = supabase.insert_schedule(tid, start, deadline, is_recurring, status, next_occurrence, frequency)
        
        # If this is a recurring task, notify the notify_user service
        if data:
            import asyncio
            asyncio.create_task(notify_schedule_added(data))
        
        return {"message":f"Task {tid} Schedule Inserted Successfully" ,"data": data}
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# Update the row
@app.put("/{sid}")
async def update_schedule(sid: str, new_data: Dict[str, Any] = Body(...)):
    try:
        # Get the current schedule data to compare changes
        current_schedule = supabase.fetch_schedule_by_sid(sid)
        if not current_schedule:
            raise HTTPException(status_code=404, detail=f"Task Schedule {sid} not found")
        
        # Check if any cron-affecting fields have changed
        has_cron_changes = has_cron_affecting_changes(current_schedule, new_data)
        
        # Update the schedule
        data = supabase.update_schedule(sid, new_data)
        if not data:
            raise HTTPException(status_code=404, detail=f"Task Schedule {sid} not found")
        
        # If cron-affecting fields have changed, notify the notify_user service
        if has_cron_changes:
            print(f"[DEBUG] Cron-affecting changes detected, notifying notify_user service")
            
            # Prepare notification data
            notify_data = {
                "sid": sid,
                "tid": current_schedule.get("tid"),
                "is_recurring": new_data.get("is_recurring", current_schedule.get("is_recurring", False)),
                "frequency": new_data.get("frequency", current_schedule.get("frequency")),
                "next_occurrence": new_data.get("next_occurrence", current_schedule.get("next_occurrence")),
                "start": new_data.get("start", current_schedule.get("start")),
                "deadline": new_data.get("deadline", current_schedule.get("deadline"))
            }
            
            # Notify asynchronously (don't wait for response)
            import asyncio
            asyncio.create_task(notify_recurring_task_updated(notify_data))
        
        return {"message":f"Task Schedule {sid} Updated Successfully" ,"data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Update up task id
@app.put("/tid/{tid}")
async def update_schedule_by_tid(tid: str, new_data: Dict[str, Any] = Body(...)):
    """Update schedule using task ID instead of schedule ID"""
    try:
        print(f"[DEBUG] Received update request for tid: {tid}")
        print(f"[DEBUG] Update data: {new_data}")
        
        # First, get the schedule to find the sid
        schedule = supabase.fetch_schedule_by_tid(tid, latest=True)
        if not schedule:
            raise HTTPException(status_code=404, detail=f"No schedule found for task {tid}")
        
        sid = schedule.get("sid")
        if not sid:
            raise HTTPException(status_code=404, detail=f"Schedule ID not found for task {tid}")
        
        print(f"[DEBUG] Found schedule sid: {sid}")
        print(f"[DEBUG] Calling supabase.update_schedule with data: {new_data}")
        
        # Check if any cron-affecting fields have changed
        has_cron_changes = has_cron_affecting_changes(schedule, new_data)
        
        # Now update using the sid
        data = supabase.update_schedule(sid, new_data)
        if not data:
            raise HTTPException(status_code=404, detail=f"Task Schedule {sid} not found")
        
        # If cron-affecting fields have changed, notify the notify_user service
        if has_cron_changes:
            print(f"[DEBUG] Cron-affecting changes detected, notifying notify_user service")
            
            # Prepare notification data
            notify_data = {
                "sid": sid,
                "tid": tid,
                "is_recurring": new_data.get("is_recurring", schedule.get("is_recurring", False)),
                "frequency": new_data.get("frequency", schedule.get("frequency")),
                "next_occurrence": new_data.get("next_occurrence", schedule.get("next_occurrence")),
                "start": new_data.get("start", schedule.get("start")),
                "deadline": new_data.get("deadline", schedule.get("deadline"))
            }
            
            # Notify asynchronously (don't wait for response)
            import asyncio
            asyncio.create_task(notify_recurring_task_updated(notify_data))
        
        # Note: Recurring task handling is now managed by the notify_user service
        # through the notification system above
        
        return {"message": f"Task {tid} Schedule Updated Successfully", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Exception in update_schedule_by_tid: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# Delete Row
@app.delete("/{sid}")
def delete_schedule(sid: str):
    data = supabase.delete_schedule(sid)
    if not data:
        raise HTTPException(status_code=404, detail="Task Schedule not found")
    return {"message": f"Task Schedule {sid} deleted successfully"}

# API endpoints for notify_user service to call
@app.get("/recurring/all")
def get_recurring_tasks_for_notify():
    """Get all recurring tasks for notify_user service"""
    try:
        recurring_tasks = supabase.fetch_recurring_tasks()
        return {"tasks": recurring_tasks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300)