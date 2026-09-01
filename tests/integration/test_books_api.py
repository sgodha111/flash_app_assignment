"""Integration tests for books API."""

from datetime import date, datetime
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.database.mongodb import MongoDB
from app.main import app


@pytest.fixture
async def client(db) -> TestClient:
    """Provide a test client."""
    settings.ENVIRONMENT = "testing"
    return TestClient(app)


class TestCreateBook:
    """Test book creation endpoint."""

    @pytest.mark.asyncio
    async def test_create_book_success(self, db, client: TestClient):
        """Test successful book creation."""
        # Create an author first
        author = {"id": 1, "name": "Mark Lutz"}
        await db["authors"].insert_one(author)

        response = await client.post(
            "/books",
            json={
                "id": 1,
                "title": "Learning Python",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 1648,
                "tags": ["Python", "Learning"],
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Learning Python"
        assert data["author_id"] == 1
        assert data["pages"] == 1648
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_book_duplicate_id(self, db, client: TestClient):
        """Test creating book with duplicate ID."""
        # Create an author
        author = {"id": 1, "name": "Mark Lutz"}
        await db["authors"].insert_one(author)

        # Create first book
        client.post(
            "/books",
            json={
                "id": 1,
                "title": "Book 1",
                "author_id": 1,
                "publisher": "Pub 1",
                "pages": 100,
            },
        )

        # Try to create another with same ID
        response = await client.post(
            "/books",
            json={
                "id": 1,
                "title": "Book 2",
                "author_id": 1,
                "publisher": "Pub 2",
                "pages": 200,
            },
        )

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_create_book_invalid_author(self, db, client: TestClient):
        """Test creating book with non-existent author."""
        response = await client.post(
            "/books",
            json={
                "id": 1,
                "title": "Learning Python",
                "author_id": 999,
                "publisher": "O'Reilly Media",
                "pages": 1648,
            },
        )

        assert response.status_code == 422


class TestGetBook:
    """Test book retrieval endpoint."""

    @pytest.mark.asyncio
    async def test_get_book_success(
        self, db, client: TestClient, sample_book_data: dict
    ):
        """Test successful book retrieval."""
        response = await client.get(f"/books/{sample_book_data['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_book_data["id"]
        assert data["title"] == sample_book_data["title"]

    @pytest.mark.asyncio
    async def test_get_book_not_found(self, client: TestClient):
        """Test retrieving non-existent book."""
        response = await client.get("/books/999")

        assert response.status_code == 404


class TestListBooks:
    """Test books list endpoint."""

    @pytest.mark.asyncio
    async def test_list_books_empty(self, db, client: TestClient):
        """Test listing books when none exist."""
        response = await client.get("/books")

        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["page"] == 1
        assert data["limit"] == 10
        assert data["total"] == 0

    @pytest.mark.asyncio
    async def test_list_books_pagination(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test books pagination."""
        response = await client.get("/books?page=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["total"] == 3

    @pytest.mark.asyncio
    async def test_list_books_filter_by_author(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test filtering books by author."""
        response = await client.get("/books?author_id=1")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert all(book["author_id"] == 1 for book in data["items"])

    @pytest.mark.asyncio
    async def test_list_books_filter_by_title(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test filtering books by title."""
        response = await client.get("/books?title=Learning")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert "Learning" in data["items"][0]["title"]

    @pytest.mark.asyncio
    async def test_list_books_filter_by_tags(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test filtering books by tags."""
        response = await client.get("/books?tags=Development")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert "Development" in data["items"][0]["tags"]

    @pytest.mark.asyncio
    async def test_list_books_combine_filters(
        self, db, client: TestClient, sample_author_with_books: dict
    ):
        """Test combining multiple filters."""
        response = await client.get("/books?author_id=1&tags=Python")

        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert all(book["author_id"] == 1 for book in data["items"])


class TestUpdateBook:
    """Test book update endpoint."""

    @pytest.mark.asyncio
    async def test_update_book_success(
        self, db, client: TestClient, sample_book_data: dict
    ):
        """Test successful book update."""
        response = await client.patch(
            f"/books/{sample_book_data['id']}",
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["id"] == sample_book_data["id"]

    @pytest.mark.asyncio
    async def test_update_book_partial(
        self, db, client: TestClient, sample_book_data: dict
    ):
        """Test partial book update."""
        original_pages = sample_book_data["pages"]

        response = await client.patch(
            f"/books/{sample_book_data['id']}",
            json={"title": "New Title"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["pages"] == original_pages  # Unchanged

    @pytest.mark.asyncio
    async def test_update_book_not_found(self, client: TestClient):
        """Test updating non-existent book."""
        response = await client.patch(
            "/books/999",
            json={"title": "New Title"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_book_invalid_author(
        self, db, client: TestClient, sample_book_data: dict
    ):
        """Test updating with invalid author."""
        response = await client.patch(
            f"/books/{sample_book_data['id']}",
            json={"author_id": 999},
        )

        assert response.status_code == 422


class TestDeleteBook:
    """Test book deletion endpoint."""

    @pytest.mark.asyncio
    async def test_delete_book_success(
        self, db, client: TestClient, sample_book_data: dict
    ):
        """Test successful book deletion."""
        response = await client.delete(f"/books/{sample_book_data['id']}")

        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/books/{sample_book_data['id']}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_book_not_found(self, client: TestClient):
        """Test deleting non-existent book."""
        response = await client.delete("/books/999")

        assert response.status_code == 404
