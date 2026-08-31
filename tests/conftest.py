"""Pytest configuration and shared fixtures."""

import asyncio
import os
from datetime import date
from typing import AsyncGenerator

import pytest

from app.config import settings
from app.database.mongodb import MongoDB


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db():
    """Provide a test database."""
    # Use test database
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DATABASE_NAME"] = "antonie_books_test"

    # Connect to MongoDB
    db_instance = await MongoDB.connect()

    # Clean up database before test
    await db_instance.client.drop_database("antonie_books_test")
    await MongoDB.connect()  # Recreate with empty database

    yield db_instance

    # Clean up after test
    await db_instance.client.drop_database("antonie_books_test")
    await MongoDB.disconnect()


@pytest.fixture
async def sample_author_data(db) -> dict:
    """Create a sample author."""
    author = {
        "id": 1,
        "name": "Mark Lutz",
        "birth_date": date(1957, 1, 1),
    }
    await db["authors"].insert_one(author)
    return author


@pytest.fixture
async def sample_book_data(db, sample_author_data: dict) -> dict:
    """Create a sample book."""
    from datetime import datetime, timezone

    book = {
        "id": 1,
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
    """Create sample authors and books."""
    from datetime import datetime, timezone

    authors = [
        {"id": 1, "name": "Mark Lutz", "birth_date": date(1957, 1, 1)},
        {"id": 2, "name": "Harry Percival", "birth_date": date(1975, 1, 1)},
        {"id": 3, "name": "No Books Author", "birth_date": date(1980, 1, 1)},
    ]
    await db["authors"].insert_many(authors)

    books = [
        {
            "id": 1,
            "title": "Learning Python",
            "author_id": 1,
            "publisher": "O'Reilly Media",
            "pages": 1648,
            "tags": ["Python", "Development"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
        {
            "id": 2,
            "title": "Python Cookbook",
            "author_id": 1,
            "publisher": "O'Reilly Media",
            "pages": 656,
            "tags": ["Python", "Recipes"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
        {
            "id": 3,
            "title": "Architecture Patterns with Python",
            "author_id": 2,
            "publisher": "O'Reilly Media",
            "pages": 304,
            "tags": ["Python", "Architecture"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    ]
    await db["books"].insert_many(books)

    return {"authors": authors, "books": books}
