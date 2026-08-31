"""Health check routes."""

import logging

from fastapi import APIRouter, Depends, HTTPException


from app.database.mongodb import get_database

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Health check endpoint.

    Returns a simple response indicating the API is running.
    """
    return {"status": "healthy", "service": "Antonie Book Catalog API"}


@router.get("/ready")
async def ready(db: "AsyncDatabase" = Depends(get_database)) -> dict:
    """Readiness check endpoint.

    Verifies the API is ready to serve requests by checking database connectivity.
    """
    try:
        # Try to run a simple database operation
        collections = await db.list_collection_names()
        return {
            "status": "ready",
            "service": "Antonie Book Catalog API",
            "database": "connected",
            "collections": len(collections),
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")
