"""Pytest configuration and shared fixtures."""

import asyncio
import os
from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest

from app.config import settings
from app.database.mongodb import MongoDB

# Counter for generating unique test IDs
_test_counter = 0


def get_unique_id():
    """Get unique test ID."""
    global _test_counter
    _test_counter += 1
    return _test_counter


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def reset_test_counter():
    """Reset test counter before each test."""
    global _test_counter
    _test_counter = 0
    yield


@pytest.fixture
async def db():
    """Provide a clean test database."""
    # Use test database
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DATABASE_NAME"] = "book_library_test"

    # Connect to MongoDB
    db_instance = await MongoDB.connect()

    # Clean up all collections before test
    for collection_name in await db_instance.list_collection_names():
        await db_instance[collection_name].delete_many({})

    yield db_instance

    # Clean up all collections after test
    for collection_name in await db_instance.list_collection_names():
        await db_instance[collection_name].delete_many({})


@pytest.fixture
async def sample_author_data(db) -> dict:
    """Create a sample author with unique ID."""
    author_id = get_unique_id()
    author = {
        "id": author_id,
        "name": "Mark Lutz",
        "birth_date": datetime(1957, 1, 1, tzinfo=timezone.utc),
    }
    await db["authors"].insert_one(author)
    return author


@pytest.fixture
async def sample_book_data(db, sample_author_data: dict) -> dict:
    """Create a sample book with unique ID."""
    from datetime import datetime, timezone

    book_id = get_unique_id()
    book = {
        "id": book_id,
        "title": "Learning Python",
        "author_id": sample_author_data["id"],
        "publisher": "O'Reilly Media",
        "pages": 1648,
        "tags": ["Python", "Development", "Learning"],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    await db["books"].insert_one(book)
    return book


@pytest.fixture
async def sample_author_with_books(db) -> dict:
    """Create sample authors and books with unique IDs."""
    base_id = get_unique_id() * 100  # Use multiplied ID to avoid collisions

    authors = [
        {"id": base_id, "name": "Mark Lutz", "birth_date": datetime(1957, 1, 1, tzinfo=timezone.utc)},
        {
            "id": base_id + 1,
            "name": "Harry Percival",
            "birth_date": datetime(1975, 1, 1, tzinfo=timezone.utc),
        },
        {
            "id": base_id + 2,
            "name": "No Books Author",
            "birth_date": datetime(1980, 1, 1, tzinfo=timezone.utc),
        },
    ]
    await db["authors"].insert_many(authors)

    books = [
        {
            "id": base_id,
            "title": "Learning Python",
            "author_id": base_id,
            "publisher": "O'Reilly Media",
            "pages": 1648,
            "tags": ["Python", "Development"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
        {
            "id": base_id + 1,
            "title": "Python Cookbook",
            "author_id": base_id,
            "publisher": "O'Reilly Media",
            "pages": 656,
            "tags": ["Python", "Recipes"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
        {
            "id": base_id + 2,
            "title": "Architecture Patterns with Python",
            "author_id": base_id + 1,
            "publisher": "O'Reilly Media",
            "pages": 304,
            "tags": ["Python", "Architecture"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    ]
    await db["books"].insert_many(books)

    return {"authors": authors, "books": books}
