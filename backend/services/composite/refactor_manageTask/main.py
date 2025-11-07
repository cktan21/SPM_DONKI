"""
Main FastAPI Application for Composite Microservice: manage-task Service
"""
import os
import logging
import pytz
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

# Import your existing components (adjust if you have these)
# from kafka_publisher import KafkaEventPublisher

# Import the delete endpoint
from workflows.task_workflow import DeleteTaskWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define UTC+8 timezone (Singapore time)
UTC_PLUS_8 = pytz.timezone('Asia/Singapore')

# Initialize Kafka publisher (if you have it)
# kafka_publisher = KafkaEventPublisher()

# Initialize FastAPI app
app = FastAPI(
    title="Composite Microservice: refactor manage-task Service",
    description="Manages task operations with member synchronization",
    version="1.0.0"
)

# CORS Configuration
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
_env_origins = os.getenv("CORS_ORIGINS")
allowed_origins = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins
    else DEFAULT_ORIGINS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-Internal-API-Key",
        "*",
    ],
    expose_headers=["*"],
    max_age=600,
)

# Configuration for external services
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://tasks:5500")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://user:5100")
PROJECTS_SERVICE_URL = os.getenv("PROJECTS_SERVICE_URL", "http://project:5200")
SCHEDULE_SERVICE_URL = os.getenv("SCHEDULE_SERVICE_URL", "http://schedule:5300")

logger.info(f"Task Service URL: {TASK_SERVICE_URL}")
logger.info(f"Users Service URL: {USERS_SERVICE_URL}")
logger.info(f"Projects Service URL: {PROJECTS_SERVICE_URL}")
logger.info(f"Schedule Service URL: {SCHEDULE_SERVICE_URL}")


# Health check endpoint
@app.get("/", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "manage-task composite service",
        "version": "2.0.0"
    }


@app.get("/health", tags=["health"])
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "task_service": TASK_SERVICE_URL,
            "users_service": USERS_SERVICE_URL,
            "projects_service": PROJECTS_SERVICE_URL,
            "schedule_service": SCHEDULE_SERVICE_URL,
        }
    }


# Delete task endpoint
@app.delete("/{task_id}", summary="Delete a task via composite service", tags=["tasks"])
async def delete_task_composite(
    task_id: str = Path(..., description="Primary key of the task (uuid)")
):
    """
    Delete a task and sync project members.
    
    Workflow:
      1) GET task details (owner, collaborators, project) BEFORE deletion
      2) DELETE task itself -> TASK_SERVICE_URL/{task_id}
      3) SYNC project members (check if users should be removed)

    Args:
        task_id: The UUID of the task to delete

    Returns:
        Dictionary containing:
        - message: Status message
        - task_id: The deleted task ID
        - task_delete: Delete operation details (url, status_code, result)
        - members_sync: Sync operation details (project_id, checked_users)

    Raises:
        HTTPException: 
            - 502: Task service errors (non-2xx/404 responses)
            - 503: Task service unavailable (network errors)
            - 500: Internal server errors

    Notes:
      - 404 from task service is treated as already deleted (idempotent).
      - Any other non-2xx/404 becomes a 502 to the client (downstream error).
    """
    logger.info(f"Starting delete workflow for task_id: {task_id}")
    
    workflow = DeleteTaskWorkflow(TASK_SERVICE_URL)
    result = await workflow.execute(task_id)
    
    logger.info(f"Delete workflow completed for task_id: {task_id}")
    return result


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 5800))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )