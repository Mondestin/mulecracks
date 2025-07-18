"""
Main API router that includes all route modules
"""
from fastapi import APIRouter

from app.api.routes import health, mule

# Create main router
router = APIRouter()

# Include route modules
router.include_router(health.router, tags=["Health"])
router.include_router(mule.router, tags=["MuleSoft Dependencies"]) 