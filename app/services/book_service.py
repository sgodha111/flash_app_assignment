"""Book service for business logic."""

import logging
from typing import List, Optional

from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookResponse, BookUpdate

logger = logging.getLogger(__name__)


class BookService:
    """Service for book operations."""

    def __init__(self, db):
        """Initialize service."""
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)

    async def create_book(self, book_create: BookCreate) -> BookResponse:
        """Create a new book."""
        # Check if book ID already exists
        if await self.book_repo.book_exists(book_create.id):
            raise ValueError(f"Book with ID {book_create.id} already exists")

        # Check if author exists
        if not await self.author_repo.author_exists(book_create.author_id):
            raise ValueError(f"Author with ID {book_create.author_id} does not exist")

        book_data = book_create.model_dump()
        created_book = await self.book_repo.create(book_data)

        return BookResponse(**created_book)

    async def get_book(self, book_id: int) -> BookResponse:
        """Get a book by ID."""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")

        return BookResponse(**book)

    async def list_books(
        self,
        page: int = 1,
        limit: int = 10,
        author_id: Optional[int] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """List books with pagination and filtering."""
        books, total = await self.book_repo.list_books(
            page=page,
            limit=limit,
            author_id=author_id,
            title=title,
            tags=tags,
        )

        return {
            "items": [BookResponse(**book) for book in books],
            "page": page,
            "limit": limit,
            "total": total,
        }

    async def update_book(self, book_id: int, book_update: BookUpdate) -> BookResponse:
        """Update a book."""
        # Check if book exists
        if not await self.book_repo.book_exists(book_id):
            raise ValueError(f"Book with ID {book_id} not found")

        # If updating author_id, verify the new author exists
        if book_update.author_id is not None:
            if not await self.author_repo.author_exists(book_update.author_id):
                raise ValueError(
                    f"Author with ID {book_update.author_id} does not exist"
                )

        # Only include fields that were explicitly set
        update_data = book_update.model_dump(exclude_unset=True)

        updated_book = await self.book_repo.update(book_id, update_data)

        if not updated_book:
            raise ValueError(f"Failed to update book with ID {book_id}")

        return BookResponse(**updated_book)

    async def delete_book(self, book_id: int) -> bool:
        """Delete a book."""
        # Check if book exists
        if not await self.book_repo.book_exists(book_id):
            raise ValueError(f"Book with ID {book_id} not found")

        deleted = await self.book_repo.delete(book_id)
        return deleted

    async def get_next_book_id(self) -> int:
        """Get the next available book ID."""
        return await self.book_repo.get_next_id()
