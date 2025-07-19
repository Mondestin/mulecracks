"""
Service for scanning MuleSoft projects and extracting flow information
"""
import os
import logging
from typing import List, Dict, Any

from app.models.flows import ProjectFlowsResponse, FlowInfo
from app.utils.flow_parser import FlowParser
from app.config.settings import settings

logger = logging.getLogger(__name__)


class FlowScanner:
    """Service class for scanning MuleSoft project flows"""
    
    def __init__(self, mule_directory: str = None):
        """
        Initialize the scanner with MuleSoft projects directory
        
        Args:
            mule_directory: Path to MuleSoft projects directory
        """
        self.mule_directory = mule_directory or settings.get_mule_directory()
        self.flow_parser = FlowParser()
    
    def scan_project_flows(self) -> ProjectFlowsResponse:
        """
        Scan all MuleSoft projects and extract flow information
        
        Returns:
            ProjectFlowsResponse with project and flow data
        """
        projects = []
        total_flows = 0
        total_endpoints = 0
        
        # Get all project directories
        project_dirs = self._get_project_directories()
        
        for project_dir in project_dirs:
            project_name = os.path.basename(project_dir)
            
            try:
                # Scan flows for this project
                project_flows = self._scan_single_project(project_dir)
                
                if project_flows:
                    project_data = {
                        "project_name": project_name,
                        "project_path": project_dir,
                        "flows": [flow.dict() for flow in project_flows],
                        "total_flows": len(project_flows),
                        "total_endpoints": sum(len(flow.endpoints) for flow in project_flows)
                    }
                    
                    projects.append(project_data)
                    total_flows += len(project_flows)
                    total_endpoints += sum(len(flow.endpoints) for flow in project_flows)
                
            except Exception as e:
                logger.error(f"Error scanning flows for project {project_name}: {str(e)}")
                continue
        
        return ProjectFlowsResponse(
            total_projects=len(projects),
            total_flows=total_flows,
            total_endpoints=total_endpoints,
            projects=projects
        )
    
    def _get_project_directories(self) -> List[str]:
        """
        Get all project directories in the MuleSoft directory
        
        Returns:
            List of project directory paths
        """
        project_dirs = []
        
        if os.path.exists(self.mule_directory):
            for item in os.listdir(self.mule_directory):
                item_path = os.path.join(self.mule_directory, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    project_dirs.append(item_path)
        
        return project_dirs
    
    def _scan_single_project(self, project_path: str) -> List[FlowInfo]:
        """
        Scan flows for a single MuleSoft project
        
        Args:
            project_path: Path to the MuleSoft project
            
        Returns:
            List of FlowInfo objects
        """
        flows = []
        
        # Find all flow files in the project
        flow_files = self.flow_parser.find_flow_files(project_path)
        
        for flow_file in flow_files:
            try:
                # Parse the flow file and get all flows
                flow_infos = self.flow_parser.parse_flow_file_all_flows(flow_file)
                if flow_infos:
                    flows.extend(flow_infos)
                    
            except Exception as e:
                logger.error(f"Error processing flow file {flow_file}: {str(e)}")
                continue
        
        return flows
    
    def get_project_flows(self, project_name: str) -> List[FlowInfo]:
        """
        Get flows for a specific project
        
        Args:
            project_name: Name of the project
            
        Returns:
            List of FlowInfo objects for the project
        """
        project_path = os.path.join(self.mule_directory, project_name)
        
        if not os.path.exists(project_path):
            raise ValueError(f"Project {project_name} not found")
        
        return self._scan_single_project(project_path)
    
    def get_endpoints_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all endpoints across projects
        
        Returns:
            Dictionary with endpoint summary statistics
        """
        response = self.scan_project_flows()
        
        endpoint_summary = {
            "total_endpoints": response.total_endpoints,
            "endpoints_by_project": {},
            "endpoint_types": {},
            "http_methods": {}
        }
        
        for project in response.projects:
            project_name = project["project_name"]
            project_endpoints = []
            
            for flow in project["flows"]:
                for endpoint in flow["endpoints"]:
                    project_endpoints.append(endpoint)
                    
                    # Count endpoint types
                    if endpoint.get("path"):
                        endpoint_type = "HTTP"
                        if endpoint.get("method"):
                            method = endpoint["method"].upper()
                            endpoint_summary["http_methods"][method] = endpoint_summary["http_methods"].get(method, 0) + 1
                    else:
                        endpoint_type = "Other"
                    
                    endpoint_summary["endpoint_types"][endpoint_type] = endpoint_summary["endpoint_types"].get(endpoint_type, 0) + 1
            
            endpoint_summary["endpoints_by_project"][project_name] = {
                "count": len(project_endpoints),
                "endpoints": project_endpoints
            }
        
        return endpoint_summary 