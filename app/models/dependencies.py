"""
Pydantic models for MuleSoft dependency data
"""
from pydantic import BaseModel
from typing import List, Optional


class DependencyInfo(BaseModel):
    """Model for individual dependency information"""
    group_id: str
    artifact_id: str
    version: str
    classifier: Optional[str] = None
    scope: Optional[str] = None


class ProjectInfo(BaseModel):
    """Model for MuleSoft project information"""
    project_name: str
    project_path: str
    group_id: str
    artifact_id: str
    version: str
    packaging: str
    app_runtime: Optional[str] = None
    mule_maven_plugin_version: Optional[str] = None
    dependencies: List[DependencyInfo]


class MuleDependencyScanResponse(BaseModel):
    """Model for the complete dependency scan response"""
    total_projects: int
    projects: List[ProjectInfo] 