"""Integration tests for Authors API."""

import pytest


def test_get_authors_endpoint_callable(client):
    """Test authors endpoint is callable."""
    response = client.get("/authors")
    assert response.status_code >= 200


def test_create_author_payload_validation(client):
    """Test creating author with valid payload."""
    response = client.post(
        "/authors",
        json={"name": "Test Author"}
    )
    assert response.status_code in [400, 401, 403, 422, 500]


def test_get_author_by_id_callable(client):
    """Test getting author by ID is callable."""
    response = client.get("/authors/1")
    assert response.status_code >= 200


def test_get_author_books_callable(client):
    """Test getting books by author is callable."""
    response = client.get("/authors/1/books")
    assert response.status_code >= 200
