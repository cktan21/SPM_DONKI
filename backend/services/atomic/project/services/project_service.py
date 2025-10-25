from typing import Dict, Any, Optional, List
from .supabaseClient import SupabaseClient


class ProjectService:
    """Service class to handle project data operations"""
    
    def __init__(self):
        self.supabase_client = SupabaseClient()

    def get_all_projects(self) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch all projects from Supabase.
        """
        return self.supabase_client.fetch_all_projects()
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a project by its ID
        """
        return self.supabase_client.fetch_project_by_pid(project_id)
    
    def get_projects_by_user_id(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get projects by user ID
        """
        return self.supabase_client.fetch_project_by_uid(user_id)
    
    def create_project(self, uid: str, name: str, desc: Optional[str] = None, members: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Create a new project
        """
        return self.supabase_client.insert_project(uid, name, desc, members)
    
    def update_project(self, project_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing project
        """
        return self.supabase_client.update_project(project_id, update_data)
    
    def delete_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Delete a project
        """
        return self.supabase_client.delete_project(project_id)
    
    def get_all_logs(self, filter_by: str = None) -> Optional[List[Dict[str, Any]]]:
        """
        Get all logs for a project
        """
        return self.supabase_client.get_all_logs(filter_by)