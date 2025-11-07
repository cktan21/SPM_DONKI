"""
Project Member Sync Service
Handles synchronization of project members after task operations.
"""
from typing import Optional, List, Dict


# Note: This function should be imported from wherever it's defined in your codebase
# For now, assuming it exists and can be imported
async def sync_project_members(
    project_id: str,
    user_ids: List[str],
    action: str
):
    """
    Sync project members - this should be imported from your existing codebase.
    
    Args:
        project_id: The project ID
        user_ids: List of user IDs to sync
        action: The action to perform (e.g., "remove", "check_remove", "add")
    """
    # This is a placeholder - import the actual implementation
    pass


class ProjectMemberSync:
    """Handles project member synchronization"""
    
    @staticmethod
    async def sync_users_for_task_deletion(
        project_id: Optional[str],
        owner: Optional[str],
        collaborators: List[str]
    ) -> Dict:
        """
        Sync project members after task deletion.
        Removes owner and collaborators from project members in a batch call.
        
        Note: This is a simple removal - for more complex logic (checking if user
        has other tasks in project), see the update_task_composite function.
        
        Args:
            project_id: The project ID (None if task has no project)
            owner: The task owner user ID
            collaborators: List of collaborator user IDs
            
        Returns:
            Dictionary with sync results containing project_id and checked_users
        """
        if not project_id:
            return {"project_id": None, "checked_users": []}
        
        # Collect all user IDs to check for removal
        users_to_check = []
        
        if owner:
            users_to_check.append(owner)
        
        if collaborators:
            users_to_check.extend(collaborators)
        
        # Check if users should be removed from project members (batch call)
        if users_to_check:
            await sync_project_members(
                project_id, users_to_check, action="remove"
            )
        
        return {
            "project_id": project_id,
            "checked_users": users_to_check,
        }