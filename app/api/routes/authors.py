"""Author API routes."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query


from app.config import settings
from app.database.mongodb import get_database
from app.schemas.author import (
    AuthorCreate,
    AuthorListResponse,
    AuthorResponse,
    AuthorWithBookCount,
)
from app.schemas.book import BookResponse
from app.schemas.error import ErrorResponse
from app.services.author_service import AuthorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/authors", tags=["authors"])


async def get_author_service(
    db: "AsyncDatabase" = Depends(get_database),
) -> AuthorService:
    """Dependency injection for author service."""
    return AuthorService(db)


@router.post(
    "",
    response_model=AuthorResponse,
    status_code=201,
    responses={409: {"model": ErrorResponse}},
)
async def create_author(
    author: AuthorCreate, service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """Create a new author."""
    try:
        return await service.create_author(author)
    except ValueError as e:
        if "already exists" in str(e):
            logger.warning(f"Duplicate author: {e}")
            raise HTTPException(status_code=409, detail=str(e))
        raise
    except Exception as e:
        logger.error(f"Error creating author: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{author_id}",
    response_model=AuthorResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    """Get an author by ID."""
    try:
        return await service.get_author(author_id)
    except ValueError as e:
        logger.warning(f"Author not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving author: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "",
    response_model=AuthorListResponse,
)
async def list_authors(
    page: int = Query(settings.DEFAULT_PAGE, ge=1),
    limit: int = Query(settings.DEFAULT_LIMIT, ge=1, le=settings.MAX_LIMIT),
    service: AuthorService = Depends(get_author_service),
) -> AuthorListResponse:
    """List authors with pagination and book count.

    **Query Parameters:**
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 10, max: 100)

    **Response includes:**
    - **book_count**: Number of books written by each author
    """
    try:
        return await service.list_authors(page=page, limit=limit)
    except Exception as e:
        logger.error(f"Error listing authors: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{author_id}/books",
    response_model=List[BookResponse],
    responses={404: {"model": ErrorResponse}},
)
async def get_author_books(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
) -> List[BookResponse]:
    """Get all books written by an author.

    Returns a list of all books by the specified author.
    """
    try:
        return await service.get_author_books(author_id)
    except ValueError as e:
        logger.warning(f"Author not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving author books: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
