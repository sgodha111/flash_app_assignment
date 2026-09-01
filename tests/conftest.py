"""Pytest configuration and fixtures for Book Library tests."""

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.mongodb import get_database


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def mock_db():
    """Create a mock MongoDB database."""
    mock_db = AsyncMock()
    mock_collection = AsyncMock()
    mock_db.__getitem__ = MagicMock(return_value=mock_collection)
    return mock_db


@pytest.fixture
def client(mock_db):
    """Create HTTP client for testing with mocked database."""
    async def override_get_database():
        return mock_db

    app.dependency_overrides[get_database] = override_get_database

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return {
        "_id": "user_123",
        "email": "test@example.com",
        "password_hash": "$2b$12$test_hash",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_author():
    """Create a sample author for testing."""
    return {
        "_id": 1,
        "name": "Test Author",
        "birth_date": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_book():
    """Create a sample book for testing."""
    return {
        "_id": 1,
        "title": "Test Book",
        "author": 1,
        "isbn": "978-0-123456-78-9",
        "pages": 300,
        "publisher": "Test Publisher",
        "year": 2024,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_books_list():
    """Create a list of sample books for pagination testing."""
    return [
        {
            "_id": i,
            "title": f"Book {i}",
            "author": 1,
            "isbn": f"978-0-123456-{i:02d}-9",
            "pages": 200 + (i * 10),
            "publisher": "Test Publisher",
            "year": 2024,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        for i in range(1, 6)
    ]
