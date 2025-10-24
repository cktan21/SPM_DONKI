from fastapi import FastAPI, HTTPException, Body
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
        recurring_tasks = schedule_client.fetch_recurring_tasks()
        for task in recurring_tasks:
            if task.get("next_occurrence") and task.get("frequency"):
                next_occurrence_dt = datetime.fromisoformat(task["next_occurrence"].replace('Z', '+00:00'))
                recurring_processor.schedule_recurring_task(task["sid"], task["frequency"], next_occurrence_dt)
        print(f"Initialized {len(recurring_tasks)} recurring tasks on startup")
    except Exception as e:
        print(f"Error initializing recurring tasks: {str(e)}")
    
    yield  # This is where the app runs
    
    # Shutdown
    recurring_processor.shutdown()

app = FastAPI(title="Composite Microservice: Notify User Service", lifespan=lifespan)
schedule_client = ScheduleClient()

@app.get("/")
def read_root():
    return {"message": "Notify User Service is running 🚀😌"}

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4500)