"""Integration tests for authors API."""

import pytest
from httpx import AsyncClient

from app.config import settings

TestClient = AsyncClient  # Alias for compatibility


class TestListAuthors:
    """Test authors list endpoint."""

    @pytest.mark.asyncio
    async def test_list_authors_with_book_count(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test listing authors with book count."""
        response = await client.get("/authors")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

        # Check author with books
        author1 = next(a for a in data["items"] if a["id"] == 1)
        assert author1["book_count"] == 2

        # Check author without books
        author3 = next(a for a in data["items"] if a["id"] == 3)
        assert author3["book_count"] == 0

    @pytest.mark.asyncio
    async def test_list_authors_pagination(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test authors pagination."""
        response = await client.get("/authors?page=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["total"] == 3


class TestGetAuthorBooks:
    """Test get author books endpoint."""

    @pytest.mark.asyncio
    async def test_get_author_books_success(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test getting books for an author."""
        response = await client.get("/authors/1/books")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(book["author_id"] == 1 for book in data)

    @pytest.mark.asyncio
    async def test_get_author_books_no_books(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test getting books for author with no books."""
        response = await client.get("/authors/3/books")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_get_author_books_not_found(self, client: TestClient):
        """Test getting books for non-existent author."""
        response = await client.get("/authors/999/books")

        assert response.status_code == 404
