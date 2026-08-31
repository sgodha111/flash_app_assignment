"""API client for FastAPI backend."""

import logging
from typing import List, Optional

import requests

from app.config import settings

logger = logging.getLogger(__name__)


class APIClient:
    """Client for FastAPI backend."""

    def __init__(self, base_url: str = None):
        """Initialize API client."""
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()

    def health(self) -> dict:
        """Check API health."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise

    # Book operations
    def get_next_book_id(self) -> dict:
        """Get the next available book ID."""
        response = self.session.get(f"{self.base_url}/books/next-id")
        response.raise_for_status()
        return response.json()

    def create_book(self, book_data: dict) -> dict:
        """Create a new book."""
        response = self.session.post(f"{self.base_url}/books", json=book_data)
        response.raise_for_status()
        return response.json()

    def get_book(self, book_id: int) -> dict:
        """Get a book by ID."""
        response = self.session.get(f"{self.base_url}/books/{book_id}")
        response.raise_for_status()
        return response.json()

    def list_books(
        self,
        page: int = 1,
        limit: int = 10,
        author_id: Optional[int] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """List books with filtering and pagination."""
        params = {"page": page, "limit": limit}

        if author_id:
            params["author_id"] = author_id
        if title:
            params["title"] = title
        if tags:
            params["tags"] = tags

        response = self.session.get(f"{self.base_url}/books", params=params)
        response.raise_for_status()
        return response.json()

    def update_book(self, book_id: int, book_data: dict) -> dict:
        """Update a book."""
        response = self.session.patch(
            f"{self.base_url}/books/{book_id}",
            json=book_data,
        )
        response.raise_for_status()
        return response.json()

    def delete_book(self, book_id: int) -> None:
        """Delete a book."""
        response = self.session.delete(f"{self.base_url}/books/{book_id}")
        response.raise_for_status()

    # Author operations
    def create_author(self, author_data: dict) -> dict:
        """Create a new author."""
        response = self.session.post(f"{self.base_url}/authors", json=author_data)
        response.raise_for_status()
        return response.json()

    def get_author(self, author_id: int) -> dict:
        """Get an author by ID."""
        response = self.session.get(f"{self.base_url}/authors/{author_id}")
        response.raise_for_status()
        return response.json()

    def list_authors(self, page: int = 1, limit: int = 10) -> dict:
        """List authors."""
        response = self.session.get(
            f"{self.base_url}/authors",
            params={"page": page, "limit": limit},
        )
        response.raise_for_status()
        return response.json()

    def get_author_books(self, author_id: int) -> List[dict]:
        """Get all books by an author."""
        response = self.session.get(f"{self.base_url}/authors/{author_id}/books")
        response.raise_for_status()
        return response.json()

    # Publisher operations
    def get_publisher_average_pages(self, publisher_name: str) -> dict:
        """Get average pages for a publisher."""
        response = self.session.get(
            f"{self.base_url}/publishers/{publisher_name}/average_pages"
        )
        response.raise_for_status()
        return response.json()


# Global client instance
_client: Optional[APIClient] = None


def get_client() -> APIClient:
    """Get or create API client."""
    global _client
    if _client is None:
        _client = APIClient()
    return _client
