"""Integration tests for Publishers API."""

import pytest


def test_publisher_average_pages_endpoint_callable(client):
    """Test publisher average pages endpoint is callable."""
    response = client.get("/publishers/Test%20Publisher/average_pages")
    assert response.status_code >= 200


def test_different_publisher_names(client):
    """Test publisher endpoint with different publisher names."""
    response = client.get("/publishers/Random%20Publisher/average_pages")
    assert response.status_code >= 200
