"""Integration tests for publishers API."""

from datetime import datetime, timezone

import pytest
from httpx import AsyncClient

from app.config import settings


class TestPublisherAveragePages:
    """Test publisher average pages endpoint."""

    @pytest.mark.asyncio
    async def test_average_pages_success(self, db, client: TestClient):
        """Test getting average pages for a publisher."""
        # Create author
        author = {"id": 1, "name": "Author 1"}
        await db["authors"].insert_one(author)

        # Create books by same publisher
        books = [
            {
                "id": 1,
                "title": "Book 1",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 300,
                "tags": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 2,
                "title": "Book 2",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 400,
                "tags": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 3,
                "title": "Book 3",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 500,
                "tags": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        ]
        await db["books"].insert_many(books)

        response = await client.get("/publishers/O'Reilly%20Media/average_pages")

        assert response.status_code == 200
        data = response.json()
        assert data["publisher"] == "O'Reilly Media"
        assert data["average_pages"] == 400.0
        assert data["book_count"] == 3

    @pytest.mark.asyncio
    async def test_average_pages_not_found(self, client: TestClient):
        """Test getting average pages for non-existent publisher."""
        response = await client.get("/publishers/NonExistent/average_pages")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_average_pages_multiple_publishers(self, db, client: TestClient):
        """Test average pages with multiple publishers."""
        # Create author
        author = {"id": 1, "name": "Author 1"}
        await db["authors"].insert_one(author)

        # Create books for different publishers
        books = [
            {
                "id": 1,
                "title": "Book 1",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 300,
                "tags": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 2,
                "title": "Book 2",
                "author_id": 1,
                "publisher": "Packt",
                "pages": 500,
                "tags": [],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        ]
        await db["books"].insert_many(books)

        # Test O'Reilly
        response1 = client.get("/publishers/O'Reilly%20Media/average_pages")
        assert response1.status_code == 200
        assert response1.json()["average_pages"] == 300.0

        # Test Packt
        response2 = client.get("/publishers/Packt/average_pages")
        assert response2.status_code == 200
        assert response2.json()["average_pages"] == 500.0
