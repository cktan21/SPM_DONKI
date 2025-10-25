from fastapi import FastAPI, HTTPException, Body
from typing import Dict, Any
from fastapi.responses import Response
from recurring_processor import recurring_processor
from schedule_client import ScheduleClient
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    try:
        all_schedules = schedule_client.fetch_all_schedules()
        
        for schedule in all_schedules:
            is_recurring = schedule.get("is_recurring")
            if is_recurring:
                if schedule.get("next_occurrence") and schedule.get("frequency"):
                    recurring_processor.schedule_recurring_task(schedule)
            if schedule.get("deadline"):
                recurring_processor.schedule_deadline_monitoring(schedule)
        print(f"Initialized {len(all_schedules)} schedules on startup")
        
    except Exception as e:
        print(f"Error initializing schedules: {str(e)}")
    
    yield  # This is where the app runs
    
    # Shutdown
    recurring_processor.shutdown()

app = FastAPI(title="Composite Microservice: Notify User Service", lifespan=lifespan)
schedule_client = ScheduleClient()

@app.get("/")
def read_root():
    return {"message": "Notify User Service is running 🚀😌"}

@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": "notify_user",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/favicon.ico")
async def get_favicon():
    return Response(status_code=204)

# Get all recurring tasks
@app.get("/task/recurring")
def get_all_recurring_tasks():
    """Get all recurring tasks from the Schedule Service"""
    try:
        recurring_tasks = schedule_client.fetch_recurring_tasks()
        return {
            "message": f"Retrieved {len(recurring_tasks)} recurring tasks",
            "tasks": recurring_tasks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recurring tasks: {str(e)}")

# Get scheduled jobs (jobs currently scheduled in the processor)
@app.get("/task/scheduled")
def get_scheduled_jobs():
    """Get all currently scheduled jobs in the Recurring Processor"""
    try:
        jobs = recurring_processor.get_scheduled_jobs()
        return {
            "message": f"Retrieved {len(jobs)} scheduled jobs",
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching scheduled jobs: {str(e)}")

# Endpoint for schedule service to notify about new recurring tasks
@app.post("/schedule/update")
def schedule_new_recurring_task(task_data: Dict[str, Any] = Body(...)):
    """Schedule a new recurring task when notified by the schedule service"""
    
    recurring_success = True
    deadline_success = True
    
    try:
        is_recurring = task_data.get("is_recurring")
        sid = task_data.get("sid")
        frequency = task_data.get("frequency")
        next_occurrence_str = task_data.get("next_occurrence")
        deadline = task_data.get("deadline")
        if is_recurring:
            if not all([sid, frequency, next_occurrence_str]):
                raise HTTPException(status_code=400, detail="Missing required fields: sid, frequency, next_occurrence")
            
            # Schedule the recurring task
            recurring_success = recurring_processor.schedule_recurring_task({
                "sid": sid,
                "frequency": frequency,
                "next_occurrence": next_occurrence_str
            })
        
        if deadline:
            deadline_success = recurring_processor.schedule_deadline_monitoring(task_data)
        
        if recurring_success and deadline_success:
            response = {
                "message": f"Successfully scheduled recurring task and deadline monitoring for task {sid}",
                "sid": sid,
                "action": "scheduled",
                "deadline_success": deadline_success
            }
            # Only include recurring_success if the task is actually recurring
            if is_recurring:
                response["recurring_success"] = recurring_success
            return response
        else:
            response = {
                "message": f"Failed to schedule recurring task or deadline monitoring for task {sid}",
                "sid": sid,
                "action": "failed"
            }
            # Only include recurring_success if the task is actually recurring
            if is_recurring:
                response["recurring_success"] = recurring_success
            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling recurring task or deadline monitoring: {str(e)}")

# Endpoint for schedule service to notify about cron job updates
@app.post("/task/recurring/update")
def update_recurring_task(task_data: Dict[str, Any] = Body(...)):
    """Update a recurring task's cron job when notified by the schedule service"""
    try:
        sid = task_data.get("sid")
        frequency = task_data.get("frequency")
        next_occurrence_str = task_data.get("next_occurrence")
        is_recurring = task_data.get("is_recurring", False)
        
        if not sid:
            raise HTTPException(status_code=400, detail="Missing required field: sid")
        
        # First, cancel any existing recurring task for this sid
        recurring_processor.cancel_recurring_task(sid)
        
        # If the task is still recurring and has the required fields, reschedule it
        if is_recurring and frequency and next_occurrence_str:
            # Schedule the updated recurring task
            success = recurring_processor.schedule_recurring_task({
                "sid": sid,
                "frequency": frequency,
                "next_occurrence": next_occurrence_str
            })
            
            if success:
                return {
                    "message": f"Successfully updated recurring task {sid}",
                    "sid": sid,
                    "frequency": frequency,
                    "next_occurrence": next_occurrence_str,
                    "action": "rescheduled"
                }
            else:
                return {
                    "message": f"Cancelled recurring task {sid} but failed to reschedule",
                    "sid": sid,
                    "action": "cancelled_only"
                }
        else:
            # Task is no longer recurring, just cancelled
            return {
                "message": f"Successfully cancelled recurring task {sid}",
                "sid": sid,
                "action": "cancelled"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating recurring task: {str(e)}")

@app.post("/task/deadline/cancel")
def cancel_deadline_monitoring(task_data: Dict[str, Any] = Body(...)):
    """Cancel deadline monitoring for a task"""
    try:
        sid = task_data.get("sid")
        
        if not sid:
            raise HTTPException(status_code=400, detail="Missing required field: sid")
        
        # Cancel the deadline monitoring
        success = recurring_processor.cancel_deadline_monitoring(sid)
        
        if success:
            return {
                "message": f"Successfully cancelled deadline monitoring for task {sid}",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel deadline monitoring")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling deadline monitoring: {str(e)}")

@app.post("/task/cancel-all")
def cancel_all_task_jobs(task_data: Dict[str, Any] = Body(...)):
    """Cancel both recurring and deadline monitoring jobs for a task"""
    try:
        sid = task_data.get("sid")
        
        if not sid:
            raise HTTPException(status_code=400, detail="Missing required field: sid")
        
        # Cancel all jobs for this task
        success = recurring_processor.cancel_all_task_jobs(sid)
        
        if success:
            return {
                "message": f"Successfully cancelled all jobs for task {sid}",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel all jobs")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling all jobs: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4500)