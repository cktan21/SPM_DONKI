"""
Task Deletion Workflow
Orchestrates the complete task deletion process including member sync.
"""
from typing import Dict
from fastapi import HTTPException

from services.task_service import TaskServiceClient
from services.project_service import ProjectMemberSync
from models.enums import HttpStatus


class DeleteTaskWorkflow:
    """Orchestrates the task deletion workflow"""
    
    def __init__(self, task_service_url: str):
        self.task_client = TaskServiceClient(task_service_url)
    
    async def execute(self, task_id: str) -> Dict:
        """
        Execute complete task deletion workflow:
        1. Get task details (owner, collaborators, project) BEFORE deletion
        2. Delete task itself
        3. Sync project members (remove users from project)
        
        Args:
            task_id: The UUID of the task to delete
            
        Returns:
            Dictionary with deletion results and sync status
            
        Notes:
            - 404 from task service is treated as already deleted (idempotent)
            - Any other non-2xx/404 becomes a 502 to the client (downstream error)
        """
        try:
            # Step 1: Get task details before deletion
            task_details = await self.task_client.get_task(task_id)
            
            if task_details is None:
                # Task doesn't exist (404) - return idempotent response
                return self._build_already_deleted_response(
                    task_id,
                    self.task_client.base_url
                )
            
            # Step 2: Delete the task
            delete_result = await self.task_client.delete_task(task_id)
            
            # Check if task was already deleted during the delete call
            if delete_result.get("already_deleted"):
                return self._build_idempotent_delete_response(
                    task_id,
                    delete_result
                )
            
            # Step 3: Sync project members (remove users from project)
            sync_result = await ProjectMemberSync.sync_users_for_task_deletion(
                task_details.project_id,
                task_details.owner,
                task_details.collaborators
            )
            
            return self._build_success_response(task_id, delete_result, sync_result)
        
        except HTTPException:
            # Re-raise HTTPExceptions from services
            raise
        except Exception as e:
            # Catch-all for unexpected errors
            raise HTTPException(
                status_code=HttpStatus.INTERNAL_ERROR.value,
                detail=f"Internal server error: {str(e)}"
            )
    
    @staticmethod
    def _build_already_deleted_response(task_id: str, base_url: str) -> Dict:
        """
        Build response for task that doesn't exist (404 on GET).
        
        Args:
            task_id: The task ID
            base_url: The task service base URL
            
        Returns:
            Idempotent deletion response
        """
        return {
            "message": "Task already deleted (idempotent)",
            "task_id": task_id,
            "task_delete": {
                "url": f"{base_url}/{task_id}",
                "status_code": HttpStatus.NOT_FOUND.value,
                "result": "already_deleted",
            },
        }
    
    @staticmethod
    def _build_idempotent_delete_response(task_id: str, delete_result: Dict) -> Dict:
        """
        Build response for task that was deleted during the DELETE call (404 on DELETE).
        
        Args:
            task_id: The task ID
            delete_result: The delete operation result
            
        Returns:
            Idempotent deletion response
        """
        return {
            "message": "Task already deleted (idempotent)",
            "task_id": task_id,
            "task_delete": {
                "url": delete_result["url"],
                "status_code": delete_result["status_code"],
                "result": delete_result["result"],
            },
        }
    
    @staticmethod
    def _build_success_response(
        task_id: str,
        delete_result: Dict,
        sync_result: Dict
    ) -> Dict:
        """
        Build successful deletion response.
        
        Args:
            task_id: The task ID
            delete_result: The delete operation result
            sync_result: The member sync result
            
        Returns:
            Success response with all operation details
        """
        return {
            "message": "Delete workflow completed and project members synced",
            "task_id": task_id,
            "task_delete": {
                "url": delete_result["url"],
                "status_code": delete_result["status_code"],
                "result": delete_result["result"],
            },
            "members_sync": sync_result,
        }