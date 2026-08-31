"""Book API routes."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query


from app.config import settings
from app.database.mongodb import get_database
from app.schemas.book import BookCreate, BookListResponse, BookResponse, BookUpdate
from app.schemas.error import ErrorResponse
from app.services.book_service import BookService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/books", tags=["books"])


async def get_book_service(db: "AsyncDatabase" = Depends(get_database)) -> BookService:
    """Dependency injection for book service."""
    return BookService(db)


@router.get(
    "/next-id",
    response_model=dict,
)
async def get_next_book_id(
    service: BookService = Depends(get_book_service),
) -> dict:
    """Get the next available book ID for auto-increment."""
    try:
        next_id = await service.get_next_book_id()
        return {"next_id": next_id}
    except Exception as e:
        logger.error(f"Error getting next book ID: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "",
    response_model=BookResponse,
    status_code=201,
    responses={
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def create_book(
    book: BookCreate, service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Create a new book.

    - **id**: Unique integer identifier (must be positive)
    - **title**: Book title (required)
    - **author_id**: ID of the book's author (must exist)
    - **publisher**: Publisher name (required)
    - **pages**: Number of pages (positive integer)
    - **tags**: List of tags (optional)
    """
    try:
        return await service.create_book(book)
    except ValueError as e:
        if "already exists" in str(e):
            logger.warning(f"Conflict creating book: {e}")
            raise HTTPException(
                status_code=409,
                detail=str(e),
            )
        elif "does not exist" in str(e):
            logger.warning(f"Validation error creating book: {e}")
            raise HTTPException(
                status_code=422,
                detail=str(e),
            )
        raise
    except Exception as e:
        logger.error(f"Error creating book: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Get a book by ID."""
    try:
        return await service.get_book(book_id)
    except ValueError as e:
        logger.warning(f"Book not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving book: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "",
    response_model=BookListResponse,
    responses={400: {"model": ErrorResponse}},
)
async def list_books(
    page: int = Query(settings.DEFAULT_PAGE, ge=1),
    limit: int = Query(settings.DEFAULT_LIMIT, ge=1, le=settings.MAX_LIMIT),
    author_id: Optional[int] = Query(None, gt=0),
    title: Optional[str] = Query(None, min_length=1),
    tags: Optional[List[str]] = Query(None),
    service: BookService = Depends(get_book_service),
) -> BookListResponse:
    """List books with pagination and filtering.

    **Query Parameters:**
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 10, max: 100)
    - **author_id**: Filter by author ID
    - **title**: Filter by book title (partial match, case-insensitive)
    - **tags**: Filter by tags (can specify multiple)

    **Example:**
    - `/books?page=1&limit=10`
    - `/books?author_id=1&page=1`
    - `/books?title=Python&limit=20`
    - `/books?tags=Python&tags=Development`
    """
    try:
        return await service.list_books(
            page=page,
            limit=limit,
            author_id=author_id,
            title=title,
            tags=tags,
        )
    except Exception as e:
        logger.error(f"Error listing books: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch(
    "/{book_id}",
    response_model=BookResponse,
    responses={
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
async def update_book(
    book_id: int,
    book_update: BookUpdate = None,
    service: BookService = Depends(get_book_service),
) -> BookResponse:
    """Update an existing book (partial update).

    Only provided fields will be updated. The `updated_at` timestamp is automatically set.

    **Request Body (all optional):**
    - **title**: New book title
    - **author_id**: New author ID (must exist)
    - **publisher**: New publisher name
    - **pages**: New page count
    - **tags**: New tags list
    """
    if book_update is None:
        book_update = BookUpdate()

    try:
        return await service.update_book(book_id, book_update)
    except ValueError as e:
        if "not found" in str(e):
            logger.warning(f"Book not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        else:
            logger.warning(f"Validation error updating book: {e}")
            raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{book_id}",
    status_code=204,
    responses={404: {"model": ErrorResponse}},
)
async def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
) -> None:
    """Delete a book by ID."""
    try:
        await service.delete_book(book_id)
    except ValueError as e:
        logger.warning(f"Book not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting book: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
