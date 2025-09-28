"""
API router configuration.
"""
from fastapi import APIRouter
from app.api.v1 import charts

api_router = APIRouter(prefix="/api")

# Include v1 routes
api_router.include_router(charts.router)