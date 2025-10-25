from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProjectBase(BaseModel):
    """Base model for project data"""
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    desc: Optional[str] = Field(None, max_length=1000, description="Project description")
    uid: str = Field(..., description="User ID who owns the project")
    members: List[str] = Field(default_factory=list, description="List of member user IDs")


class ProjectCreate(ProjectBase):
    """Model for creating a new project"""
    pass


class ProjectUpdate(BaseModel):
    """Model for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    desc: Optional[str] = Field(None, max_length=1000)
    uid: Optional[str] = None
    members: Optional[List[str]] = None


class Project(ProjectBase):
    """Complete project model with all fields"""
    id: str = Field(..., description="Project ID")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    """Response model for project operations"""
    message: str
    project: Optional[Project] = None
    data: Optional[dict] = None


class ProjectListResponse(BaseModel):
    """Response model for project list operations"""
    message: str
    project: Optional[list[Project]] = None
