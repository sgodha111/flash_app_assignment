"""Publisher API routes."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.database.mongodb import get_database
from app.schemas.error import ErrorResponse
from app.services.publisher_service import PublisherService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publishers", tags=["publishers"])


class PublisherAverageResponse(BaseModel):
    """Average pages response."""

    publisher: str
    average_pages: float
    book_count: Optional[int] = None


async def get_publisher_service(
    db: "AsyncDatabase" = Depends(get_database),
) -> PublisherService:
    """Dependency injection for publisher service."""
    return PublisherService(db)


@router.get(
    "/{publisher_name}/average_pages",
    response_model=PublisherAverageResponse,
    responses={404: {"model": ErrorResponse}},
)
async def get_publisher_average_pages(
    publisher_name: str,
    service: PublisherService = Depends(get_publisher_service),
) -> PublisherAverageResponse:
    """Get average pages for books by a publisher.

    Uses MongoDB aggregation pipeline to calculate the average number of pages
    for all books published by the specified publisher.

    **Parameters:**
    - **publisher_name**: Name of the publisher

    **Returns:**
    - **publisher**: Publisher name
    - **average_pages**: Average number of pages across all books
    - **book_count**: Total number of books by this publisher
    """
    try:
        average = await service.get_average_pages(publisher_name)

        if average is None:
            logger.warning(f"No books found for publisher: {publisher_name}")
            raise HTTPException(
                status_code=404,
                detail=f"No books found for publisher: {publisher_name}",
            )

        # Get book count
        books_collection = service.db["books"]
        book_count = await books_collection.count_documents(
            {"publisher": publisher_name}
        )

        return PublisherAverageResponse(
            publisher=publisher_name,
            average_pages=round(average, 2),
            book_count=book_count,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating average pages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
