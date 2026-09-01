"""Book repository for database access."""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class BookRepository:
    """Repository for book database operations."""

    def __init__(self, db):
        """Initialize repository."""
        self.db = db
        self.collection = db["books"]

    async def create(self, book_data: dict) -> dict:
        """Create a new book."""
        book_data["created_at"] = datetime.now(timezone.utc)
        book_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(book_data)
        logger.debug(f"Created book with ID {book_data['id']}")
        return {**book_data, "_id": result.inserted_id}

    async def get_by_id(self, book_id: int) -> Optional[dict]:
        """Get a book by ID."""
        book = await self.collection.find_one({"id": book_id})
        logger.debug(f"Retrieved book with ID {book_id}: {book is not None}")
        return book

    async def list_books(
        self,
        page: int = 1,
        limit: int = 10,
        author_id: Optional[int] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Tuple[List[dict], int]:
        """List books with pagination and filtering."""
        query = {}

        if author_id:
            query["author_id"] = author_id

        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        if tags:
            query["tags"] = {"$in": tags}

        skip = (page - 1) * limit
        books = await self.collection.find(query).skip(skip).limit(limit).to_list(limit)

        total = await self.collection.count_documents(query)

        logger.debug(f"Listed {len(books)} books (total: {total})")
        return books, total

    async def update(self, book_id: int, update_data: dict) -> Optional[dict]:
        """Update a book."""
        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            {"id": book_id},
            {"$set": update_data},
            return_document=True,
        )

        logger.debug(f"Updated book with ID {book_id}")
        return result

    async def delete(self, book_id: int) -> bool:
        """Delete a book."""
        result = await self.collection.delete_one({"id": book_id})
        logger.debug(f"Deleted book with ID {book_id}")
        return result.deleted_count > 0

    async def book_exists(self, book_id: int) -> bool:
        """Check if a book exists."""
        book = await self.collection.find_one({"id": book_id}, projection={"_id": 1})
        return book is not None

    async def get_by_author_id(self, author_id: int) -> List[dict]:
        """Get all books by an author."""
        books = await self.collection.find({"author_id": author_id}).to_list(None)
        logger.debug(f"Retrieved {len(books)} books for author {author_id}")
        return books

    async def get_next_id(self) -> int:
        """Get the next available book ID (auto-increment)."""
        book = await self.collection.find_one(sort=[("id", -1)])
        if book:
            next_id = book["id"] + 1
        else:
            next_id = 1
        logger.debug(f"Next book ID: {next_id}")
        return next_id
