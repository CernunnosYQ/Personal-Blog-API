import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.jwt import create_access_token, create_refresh_token, verify_access_token
from app.models import User


def test_create_access_token() -> None:
    """Test creating an access token."""
    sub = "testuser"
    token = create_access_token(sub=sub)
    assert (
        isinstance(token, str) and len(token) > 0
    ), "Token should be a non-empty string"

    decoded_data = verify_access_token(token)
    assert decoded_data["sub"] == sub, "Decoded token data should match input data"


def test_get_current_user(
    client: TestClient, db_session: Session, test_user: User
) -> None:
    """Test getting the current user from a valid token."""

    response = client.post(
        "/api/login",
        data={"username": test_user.username, "password": "SecurePassword123"},
        headers={"user-agent": "test-agent"},
    )
    assert response.status_code == 200, "Login should be successful"
    access_token = response.json()["data"].get("access_token")

    current_user = get_current_user(token=access_token, db=db_session)
    assert current_user is not None, "Current user should not be None"

    assert current_user.id == test_user.id, "Current user ID should match test user"
    assert (
        current_user.username == test_user.username
    ), "Current user username should match test user"


def test_create_refresh_token() -> None:
    """Test creating an access token."""
    sub = "testuser"
    fingerprint = "3f1c838b9f6a05f4b482e8f3a6a4a243"

    token = create_refresh_token(sub=sub, fingerprint=fingerprint)
    assert (
        isinstance(token, str) and len(token) > 0
    ), "Token should be a non-empty string"

    decoded_data = verify_access_token(token)
    assert decoded_data["sub"] == sub, "Decoded token data should match input data"
    assert (
        decoded_data["fingerprint"] == fingerprint
    ), "Decoded token IP should match input IP"


def test_verify_access_token_invalid() -> None:
    """Test verifying an invalid access token."""
    invalid_token = "this.is.not.a.valid.token"

    with pytest.raises(ValueError, match="Invalid or expired token"):
        verify_access_token(invalid_token)


def test_login_success(client: TestClient, test_user: User) -> None:
    """Test de login exitoso con usuario de prueba."""

    response = client.post(
        "/api/login",
        data={"username": test_user.username, "password": "SecurePassword123"},
        headers={"user-agent": "test-agent"},
    )

    access_token = response.json()["data"].get("access_token")

    assert response.status_code == 200
    assert isinstance(verify_access_token(access_token), dict)
    assert "refresh_token" in response.cookies


def test_logout_success(client: TestClient, test_user: User) -> None:
    """Test de logout exitoso."""
    response = client.post(
        "/api/login",
        data={"username": test_user.username, "password": "SecurePassword123"},
        headers={"user-agent": "test-agent"},
    )
    assert response.status_code == 200

    response = client.post("/api/logout")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "refresh_token" not in response.cookies
    assert "access_token" not in response.cookies


def test_refresh_token_success(client: TestClient, test_user: User) -> None:
    """Test de refresh token exitoso."""
    device_fingerprint = "3f1c838b9f6a05f4b482e8f3a6a4a243"

    response = client.post(
        "/api/login",
        data={"username": test_user.username, "password": "SecurePassword123"},
        headers={"x-Device-Fingerprint": device_fingerprint},
    )
    assert response.status_code == 200

    refresh_token = response.cookies.get("refresh_token")
    client.cookies.set("refresh_token", refresh_token)

    access_token = response.json()["data"].get("access_token")

    time.sleep(1)

    response = client.post(
        "/api/refresh",
        headers={
            "Authorization": f"Bearer {access_token}",
            "x-Device-Fingerprint": device_fingerprint,
        },
    )

    new_access_token = response.json()["data"].get("access_token")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert new_access_token != access_token, "Access token should be refreshed"
