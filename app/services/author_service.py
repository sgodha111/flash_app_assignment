"""Author service for business logic."""

import logging
from typing import List



from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorWithBookCount
from app.schemas.book import BookResponse

logger = logging.getLogger(__name__)


class AuthorService:
    """Service for author operations."""

    def __init__(self, db):
        """Initialize service."""
        self.author_repo = AuthorRepository(db)
        self.book_repo = BookRepository(db)

    async def create_author(self, author_create: AuthorCreate) -> AuthorResponse:
        """Create a new author."""
        # Check if author ID already exists
        if await self.author_repo.author_exists(author_create.id):
            raise ValueError(f"Author with ID {author_create.id} already exists")

        author_data = author_create.model_dump()
        created_author = await self.author_repo.create(author_data)

        return AuthorResponse(**created_author)

    async def get_author(self, author_id: int) -> AuthorResponse:
        """Get an author by ID."""
        author = await self.author_repo.get_by_id(author_id)
        if not author:
            raise ValueError(f"Author with ID {author_id} not found")

        return AuthorResponse(**author)

    async def list_authors(self, page: int = 1, limit: int = 10) -> dict:
        """List authors with pagination and book count."""
        authors, total = await self.author_repo.get_with_book_count(
            page=page, limit=limit
        )

        return {
            "items": [AuthorWithBookCount(**author) for author in authors],
            "page": page,
            "limit": limit,
            "total": total,
        }

    async def get_author_books(self, author_id: int) -> List[BookResponse]:
        """Get all books by an author."""
        # Check if author exists
        if not await self.author_repo.author_exists(author_id):
            raise ValueError(f"Author with ID {author_id} not found")

        books = await self.book_repo.get_by_author_id(author_id)

        return [BookResponse(**book) for book in books]
