from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from models import Project, ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from services.project_service import ProjectService


class ProjectController:
    """Controller class to handle project business logic"""
    
    def __init__(self):
        self.project_service = ProjectService()
        # 👇 cache Project model fields (Pydantic v2)
        self._project_fields = set(Project.model_fields.keys())

    # Get all projects
    def get_all_projects(self) -> ProjectListResponse:
        """
        Retrieve all projects from Supabase.
        """
        try:
            projects_data = self.project_service.get_all_projects() or []

            # Inline fix: replace None members with []
            projects = [
                Project(**{**p, "members": p.get("members") or []})
                for p in projects_data
            ]

            if not projects:
                return ProjectListResponse(message="No projects found", project=[])

            return ProjectListResponse(
                message=f"{len(projects)} project(s) retrieved",
                project=projects
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        

    # 👇 ADD THIS HELPER
    def _project_from_row(self, row: Dict[str, Any]) -> Project:
        """
        Build a Project model from an arbitrary DB row, ignoring unknown keys
        (e.g. owner_department from a view). Ensures members is a list.
        """
        safe = {k: v for k, v in row.items() if k in self._project_fields}
        # normalize members
        if "members" in self._project_fields:
            safe["members"] = row.get("members") or []
        return Project(**safe)

    #Get all projects by Department
    def get_all_projects_by_dept(self, department: str) -> ProjectListResponse:
        try:
            projects_data = self.project_service.get_all_projects_by_dept(department) or []
            projects = [self._project_from_row(p) for p in projects_data]

            if not projects:
                return ProjectListResponse(
                    message=f"No projects found for department '{department}'",
                    project=[]
                )

            return ProjectListResponse(
                    message=f"{len(projects)} project(s) retrieved for department '{department}'",
                    project=projects
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching projects by department: {str(e)}"
            )


    def get_project_by_id(self, project_id: str) -> ProjectResponse:
        """
        Get a project by its ID
        Returns the project data if found, raises HTTPException if not found
        """
        try:
            project_data = self.project_service.get_project_by_id(project_id)
            if project_data:
                project = Project(**project_data)
                return ProjectResponse(
                    message=f"Project with Project ID {project_id} retrieved successfully",
                    project=project
                )
            else:
                raise HTTPException(status_code=404, detail=f"Project with Project ID {project_id} not found")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error querying project {project_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_projects_by_user_id(self, user_id: str) -> ProjectListResponse:
        """
        Get projects by user ID
        Returns the project data if found, raises HTTPException if not found
        """
        try:
            projects_data = self.project_service.get_projects_by_user_id(user_id)
            if projects_data and len(projects_data) > 0:
                projects = [Project(**project) for project in projects_data]
                return ProjectListResponse(
                    message=f"Projects with user id {user_id} retrieved successfully",
                    project=projects
                )
            else:
                raise HTTPException(status_code=404, detail=f"Project with user id {user_id} not found")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error querying project {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def create_project(self, project_data: Dict[str, Any]) -> ProjectResponse:
        """
        Create a new project
        """
        try:
            # Validate required fields
            if not project_data.get("uid"):
                raise HTTPException(status_code=400, detail="uid is required")
            if not project_data.get("name"):
                raise HTTPException(status_code=400, detail="name is required")
            
            # Create project using service
            created_data = self.project_service.create_project(
                uid=project_data["uid"],
                name=project_data["name"],
                desc=project_data.get("desc"),
                members=project_data.get("members", [])
                
            )
            
            if created_data:
                project = Project(**created_data)
                return ProjectResponse(
                    message="Project Inserted Successfully",
                    project=project,
                    data=created_data
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to create project")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def update_project(self, project_id: str, update_data: Dict[str, Any]) -> ProjectResponse:
        """
        Update an existing project
        """
        if not update_data:
            raise HTTPException(status_code=400, detail="Update payload cannot be empty")
        
        try:
            updated_data = self.project_service.update_project(project_id, update_data)
            if updated_data:
                project = Project(**updated_data)
                return ProjectResponse(
                    message=f"Project {project_id} Project Updated Successfully",
                    project=project,
                    data=updated_data
                )
            else:
                raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def delete_project(self, project_id: str) -> Dict[str, str]:
        """
        Delete a project
        """
        try:
            deleted_data = self.project_service.delete_project(project_id)
            if deleted_data:
                return {"message": f"Project {project_id} deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Project not found")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    def get_all_logs(self, filter_by: str = None) -> List[Dict[str, Any]]:
        """
        Get all logs for a project
        """
        return self.project_service.get_all_logs(filter_by)
    
    
    def get_projects_by_department(self, department: str) -> ProjectListResponse:
        """
        Get projects by department
        """
        return self.project_service.get_projects_by_department(department)