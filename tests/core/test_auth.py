import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.models import User
from app.utils.jwt import create_access_token, create_refresh_token, verify_access_token


def test_create_access_token() -> None:
    """Test creating an access token."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert (
        isinstance(token, str) and len(token) > 0
    ), "Token should be a non-empty string"

    decoded_data = verify_access_token(token)
    assert (
        decoded_data["sub"] == "testuser"
    ), "Decoded token data should match input data"


def test_get_current_user(db_session: Session, test_user: User) -> None:
    """Test getting the current user from a valid token."""

    token = create_access_token({"user_id": test_user.id})
    current_user = get_current_user(token=token, db=db_session)

    assert current_user.id == test_user.id, "Current user ID should match test user"
    assert (
        current_user.username == test_user.username
    ), "Current user username should match test user"


def test_create_refresh_token() -> None:
    """Test creating an access token."""
    data = {"sub": "testuser", "ip": "0.0.0.0"}
    token = create_refresh_token(data)
    assert (
        isinstance(token, str) and len(token) > 0
    ), "Token should be a non-empty string"

    decoded_data = verify_access_token(token)
    assert (
        decoded_data["sub"] == "testuser"
    ), "Decoded token data should match input data"
    assert decoded_data["ip"] == "0.0.0.0", "Decoded token IP should match input IP"


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

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "refresh_token" in response.cookies
    assert "access_token" in response.cookies
