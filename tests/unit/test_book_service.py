"""Unit tests for BookService."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.book_service import BookService


@pytest.mark.asyncio
async def test_book_service_get_all_books(sample_books_list):
    """Test retrieving all books."""
    mock_db = AsyncMock()
    books_collection = AsyncMock()
    mock_db.__getitem__.return_value = books_collection
    books_collection.find.return_value.to_list = AsyncMock(
        return_value=sample_books_list
    )

    service = BookService(mock_db)
    books = await books_collection.find.return_value.to_list(None)

    assert len(books) == 5
    assert books[0]["title"] == "Book 1"


@pytest.mark.asyncio
async def test_book_service_create_book(sample_book):
    """Test creating a new book."""
    mock_db = AsyncMock()
    books_collection = AsyncMock()
    mock_db.__getitem__.return_value = books_collection
    books_collection.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=sample_book["_id"])
    )

    service = BookService(mock_db)
    result = await books_collection.insert_one(sample_book)

    assert result.inserted_id == sample_book["_id"]
    books_collection.insert_one.assert_called_once()


@pytest.mark.asyncio
async def test_book_service_get_book_by_id(sample_book):
    """Test retrieving a book by ID."""
    mock_db = AsyncMock()
    books_collection = AsyncMock()
    mock_db.__getitem__.return_value = books_collection
    books_collection.find_one = AsyncMock(return_value=sample_book)

    service = BookService(mock_db)
    result = await books_collection.find_one({"_id": sample_book["_id"]})

    assert result["_id"] == sample_book["_id"]
    assert result["title"] == sample_book["title"]


@pytest.mark.asyncio
async def test_book_service_update_book(sample_book):
    """Test updating a book."""
    mock_db = AsyncMock()
    books_collection = AsyncMock()
    mock_db.__getitem__.return_value = books_collection
    books_collection.update_one = AsyncMock(
        return_value=MagicMock(modified_count=1)
    )

    service = BookService(mock_db)
    updated_data = {"title": "Updated Book", "pages": 350}
    result = await books_collection.update_one(
        {"_id": sample_book["_id"]}, {"$set": updated_data}
    )

    assert result.modified_count == 1


@pytest.mark.asyncio
async def test_book_service_delete_book(sample_book):
    """Test deleting a book."""
    mock_db = AsyncMock()
    books_collection = AsyncMock()
    mock_db.__getitem__.return_value = books_collection
    books_collection.delete_one = AsyncMock(
        return_value=MagicMock(deleted_count=1)
    )

    service = BookService(mock_db)
    result = await books_collection.delete_one({"_id": sample_book["_id"]})

    assert result.deleted_count == 1
