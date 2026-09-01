"""Author repository for database access."""

import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class AuthorRepository:
    """Repository for author database operations."""

    def __init__(self, db):
        """Initialize repository."""
        self.db = db
        self.collection = db["authors"]

    async def create(self, author_data: dict) -> dict:
        """Create a new author."""
        from datetime import date

        # Prepare data for MongoDB - convert date objects to strings
        db_data = author_data.copy()
        if db_data.get("birth_date") and isinstance(db_data["birth_date"], date):
            db_data["birth_date"] = db_data["birth_date"].isoformat()

        result = await self.collection.insert_one(db_data)
        logger.debug(f"Created author with ID {db_data['id']}")
        return {**author_data, "_id": result.inserted_id}

    async def get_by_id(self, author_id: int) -> Optional[dict]:
        """Get an author by ID."""
        author = await self.collection.find_one({"id": author_id})
        logger.debug(f"Retrieved author with ID {author_id}: {author is not None}")
        return author

    async def list_authors(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[List[dict], int]:
        """List authors with pagination."""
        skip = (page - 1) * limit
        authors = await self.collection.find().skip(skip).limit(limit).to_list(limit)

        total = await self.collection.count_documents({})

        logger.debug(f"Listed {len(authors)} authors (total: {total})")
        return authors, total

    async def author_exists(self, author_id: int) -> bool:
        """Check if an author exists."""
        author = await self.collection.find_one(
            {"id": author_id}, projection={"_id": 1}
        )
        return author is not None

    async def list_all_with_book_count(self) -> List[dict]:
        """List all authors with book count using aggregation."""
        pipeline = [
            {
                "$lookup": {
                    "from": "books",
                    "localField": "id",
                    "foreignField": "author_id",
                    "as": "books",
                }
            },
            {"$addFields": {"book_count": {"$size": "$books"}}},
            {"$project": {"books": 0}},
            {"$sort": {"id": 1}},
        ]

        result = await self.collection.aggregate(pipeline).to_list(None)
        logger.debug(f"Retrieved {len(result)} authors with book counts")
        return result

    async def get_with_book_count(
        self, page: int = 1, limit: int = 10
    ) -> Tuple[List[dict], int]:
        """List authors with book count using pagination."""
        skip = (page - 1) * limit

        pipeline = [
            {
                "$lookup": {
                    "from": "books",
                    "localField": "id",
                    "foreignField": "author_id",
                    "as": "books",
                }
            },
            {"$addFields": {"book_count": {"$size": "$books"}}},
            {"$project": {"books": 0}},
            {"$sort": {"id": 1}},
            {
                "$facet": {
                    "metadata": [{"$count": "total"}],
                    "data": [
                        {"$skip": skip},
                        {"$limit": limit},
                    ],
                }
            },
        ]

        result = await self.collection.aggregate(pipeline).to_list(None)

        if not result:
            return [], 0

        data = result[0].get("data", [])
        metadata = result[0].get("metadata", [])
        total = metadata[0]["total"] if metadata else 0

        logger.debug(f"Retrieved {len(data)} authors with pagination (total: {total})")
        return data, total
