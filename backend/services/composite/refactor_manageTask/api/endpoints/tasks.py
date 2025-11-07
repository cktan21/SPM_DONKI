"""
Task Management Endpoints
Handles task-related operations including deletion with member sync.
"""
import logging
from fastapi import APIRouter, Path, HTTPException
from workflows.task_workflow import DeleteTaskWorkflow
import os

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/tasks", tags=["tasks"])

TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://tasks:5500")


@router.delete("/{task_id}", summary="Delete a task via composite service")
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
    
    try:
        workflow = DeleteTaskWorkflow(TASK_SERVICE_URL)
        result = await workflow.execute(task_id)
        
        logger.info(f"Delete workflow completed for task_id: {task_id}")
        return result
    
    except HTTPException as e:
        logger.error(f"Delete workflow failed for task_id: {task_id} - {e.detail}")
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error in delete workflow for task_id: {task_id}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )