"""
Pydantic models for MuleSoft flow and endpoint data
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class EndpointInfo(BaseModel):
    """Model for individual endpoint information"""
    name: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None
    doc_id: Optional[str] = None
    config_ref: Optional[str] = None
    listener_config: Optional[Dict[str, Any]] = None


class FlowInfo(BaseModel):
    """Model for individual flow information"""
    name: str
    file_path: str
    endpoints: List[EndpointInfo]
    processors_count: int
    error_handlers: List[str]
    sub_flows: List[str]


class ProjectFlowsResponse(BaseModel):
    """Model for the complete flows scan response"""
    total_projects: int
    total_flows: int
    total_endpoints: int
    projects: List[Dict[str, Any]] 