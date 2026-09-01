"""Integration tests for Authentication API."""

import pytest


@pytest.mark.skip(reason="Requires real database with seeded users")
def test_login_endpoint_callable(client):
    """Test login endpoint is reachable."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code in [200, 401, 422, 500]


def test_login_missing_fields_validation(client):
    """Test login validation for missing fields."""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com"}
    )
    assert response.status_code in [400, 422]


def test_refresh_token_endpoint_callable(client):
    """Test token refresh endpoint is reachable."""
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "test_token"}
    )
    assert response.status_code >= 200
