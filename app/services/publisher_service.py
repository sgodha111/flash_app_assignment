"""Publisher service for business logic."""

import logging
from typing import Optional



logger = logging.getLogger(__name__)


class PublisherService:
    """Service for publisher operations."""

    def __init__(self, db):
        """Initialize service."""
        self.db = db

    async def get_average_pages(self, publisher_name: str) -> Optional[float]:
        """Get average pages for books by a publisher using aggregation."""
        pipeline = [
            {
                "$match": {
                    "publisher": publisher_name
                }
            },
            {
                "$group": {
                    "_id": "$publisher",
                    "average_pages": {"$avg": "$pages"},
                    "book_count": {"$sum": 1},
                }
            },
        ]

        result = await self.db["books"].aggregate(pipeline).to_list(1)

        if not result:
            logger.info(f"No books found for publisher: {publisher_name}")
            return None

        avg_pages = result[0].get("average_pages")
        logger.debug(
            f"Average pages for {publisher_name}: {avg_pages} "
            f"({result[0].get('book_count')} books)"
        )

        return avg_pages
