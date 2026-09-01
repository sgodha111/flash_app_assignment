"""Integration tests for API health endpoints."""

import pytest


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data or data.get("status") == "healthy"


def test_docs_endpoint(client):
    """Test API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint(client):
    """Test ReDoc documentation endpoint."""
    response = client.get("/redoc")
    assert response.status_code == 200
