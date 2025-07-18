"""
Health check routes
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    """Root endpoint that returns a welcome message"""
    return {
        "message": "Welcome to Mule Cracks!", 
        "status": "running"
    }


@router.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify the API is running"""
    return {
        "status": "healthy", 
        "message": "API is running successfully"
    } 