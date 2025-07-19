"""
MuleSoft flow scanning routes
"""
from fastapi import APIRouter, HTTPException
import logging

from app.models.flows import ProjectFlowsResponse
from app.services.flow_scanner import FlowScanner

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/mule/flows", response_model=ProjectFlowsResponse)
async def get_mule_flows():
    """
    Scan all MuleSoft projects and return flow information and endpoints
    """
    try:
        scanner = FlowScanner()
        result = scanner.scan_project_flows()
        return result
    except Exception as e:
        logger.error(f"Error scanning MuleSoft flows: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error scanning MuleSoft flows: {str(e)}"
        )


@router.get("/mule/flows/{project_name}")
async def get_project_flows(project_name: str):
    """
    Get flows for a specific MuleSoft project
    """
    try:
        scanner = FlowScanner()
        flows = scanner.get_project_flows(project_name)
        return {
            "project_name": project_name,
            "flows": [flow.dict() for flow in flows],
            "total_flows": len(flows),
            "total_endpoints": sum(len(flow.endpoints) for flow in flows)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting flows for project {project_name}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error getting flows for project {project_name}: {str(e)}"
        )


@router.get("/mule/endpoints/summary")
async def get_endpoints_summary():
    """
    Get a summary of all endpoints across all MuleSoft projects
    """
    try:
        scanner = FlowScanner()
        summary = scanner.get_endpoints_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting endpoints summary: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error getting endpoints summary: {str(e)}"
        ) 