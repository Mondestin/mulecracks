"""
MuleSoft dependency scanning routes
"""
from fastapi import APIRouter, HTTPException
import logging

from app.models.dependencies import MuleDependencyScanResponse
from app.services.mule_scanner import MuleProjectScanner

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/mule/dependencies", response_model=MuleDependencyScanResponse)
async def get_mule_dependencies():
    """
    Scan all MuleSoft projects and return dependency versions and related data
    """
    try:
        scanner = MuleProjectScanner()
        result = scanner.scan_projects()
        return result
    except Exception as e:
        logger.error(f"Error scanning MuleSoft projects: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error scanning MuleSoft projects: {str(e)}"
        ) 