"""Unit tests for book service."""

import pytest
from datetime import datetime, timezone

from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService


@pytest.mark.asyncio
class TestBookService:
    """Test book service."""

    async def test_create_book_success(self, db, sample_author_data: dict):
        """Test successful book creation."""
        service = BookService(db)

        book_create = BookCreate(
            id=1,
            title="Learning Python",
            author_id=sample_author_data["id"],
            publisher="O'Reilly Media",
            pages=1648,
            tags=["Python", "Learning"],
        )

        result = await service.create_book(book_create)

        assert isinstance(result, BookResponse)
        assert result.id == 1
        assert result.title == "Learning Python"
        assert result.author_id == sample_author_data["id"]

    async def test_create_book_duplicate_id(self, db, sample_book_data: dict):
        """Test creating book with duplicate ID."""
        service = BookService(db)

        book_create = BookCreate(
            id=sample_book_data["id"],  # Duplicate
            title="Another Book",
            author_id=sample_book_data["author_id"],
            publisher="Publisher",
            pages=100,
        )

        with pytest.raises(ValueError, match="already exists"):
            await service.create_book(book_create)

    async def test_create_book_invalid_author(self, db):
        """Test creating book with non-existent author."""
        service = BookService(db)

        book_create = BookCreate(
            id=1,
            title="Some Book",
            author_id=999,  # Non-existent
            publisher="Publisher",
            pages=100,
        )

        with pytest.raises(ValueError, match="does not exist"):
            await service.create_book(book_create)

    async def test_get_book_success(self, db, sample_book_data: dict):
        """Test getting an existing book."""
        service = BookService(db)

        result = await service.get_book(sample_book_data["id"])

        assert isinstance(result, BookResponse)
        assert result.id == sample_book_data["id"]
        assert result.title == sample_book_data["title"]

    async def test_get_book_not_found(self, db):
        """Test getting non-existent book."""
        service = BookService(db)

        with pytest.raises(ValueError, match="not found"):
            await service.get_book(999)

    async def test_list_books_empty(self, db):
        """Test listing books when none exist."""
        service = BookService(db)

        result = await service.list_books()

        assert result["items"] == []
        assert result["total"] == 0
        assert result["page"] == 1

    async def test_list_books_with_pagination(self, db, sample_author_with_books: dict):
        """Test listing books with pagination."""
        service = BookService(db)

        result = await service.list_books(page=1, limit=2)

        assert len(result["items"]) == 2
        assert result["total"] == 3
        assert result["page"] == 1
        assert result["limit"] == 2

    async def test_list_books_filter_by_author(self, db, sample_author_with_books: dict):
        """Test filtering books by author."""
        service = BookService(db)

        result = await service.list_books(author_id=1)

        assert len(result["items"]) == 2
        assert all(book.author_id == 1 for book in result["items"])

    async def test_update_book_success(self, db, sample_book_data: dict):
        """Test successful book update."""
        service = BookService(db)

        book_update = BookUpdate(title="Updated Title")
        result = await service.update_book(sample_book_data["id"], book_update)

        assert isinstance(result, BookResponse)
        assert result.title == "Updated Title"
        assert result.id == sample_book_data["id"]

    async def test_update_book_partial(self, db, sample_book_data: dict):
        """Test partial book update doesn't change other fields."""
        service = BookService(db)

        original_pages = sample_book_data["pages"]
        book_update = BookUpdate(title="New Title")
        result = await service.update_book(sample_book_data["id"], book_update)

        assert result.title == "New Title"
        assert result.pages == original_pages

    async def test_update_book_not_found(self, db):
        """Test updating non-existent book."""
        service = BookService(db)

        book_update = BookUpdate(title="New Title")

        with pytest.raises(ValueError, match="not found"):
            await service.update_book(999, book_update)

    async def test_delete_book_success(self, db, sample_book_data: dict):
        """Test successful book deletion."""
        service = BookService(db)

        result = await service.delete_book(sample_book_data["id"])

        assert result is True

        # Verify deletion
        with pytest.raises(ValueError):
            await service.get_book(sample_book_data["id"])

    async def test_delete_book_not_found(self, db):
        """Test deleting non-existent book."""
        service = BookService(db)

        with pytest.raises(ValueError, match="not found"):
            await service.delete_book(999)
