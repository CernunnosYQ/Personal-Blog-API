import pytest

from fastapi import status
from app.crud import crud_get_user


def test_crud_get_user_raises_value_error_if_not_user_or_id(db_session):
    """Test creating a user with missing id."""

    with pytest.raises(ValueError, match="Either id or username must be provided."):
        crud_get_user(db=db_session)


def test_get_user_success(client, db_session, test_user):
    """Test retrieving a user by username and ID."""

    username = test_user.username
    user_id = test_user.id

    response = client.get(f"/api/get/user/{username}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Expected successful user retrieval"
    data = response.json().get("data", {})
    assert (
        data["username"] == test_user.username
    ), "Username should match the created user"
    assert data["email"] == test_user.email, "Email should match the created user"

    response = client.get(f"/api/get/user/{user_id}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Expected successful user retrieval"
    data = response.json().get("data", {})
    assert data["id"] == user_id, "User ID should match the requested ID"
    assert data["email"] == test_user.email, "Email should match the created user"


def test_get_user_not_found(client, db_session):
    """Test retrieving a user that does not exist."""

    response = client.get("/api/get/user/nonexistentuser")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user"

    response = client.get("/api/get/user/999999")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user ID"


def test_get_user_invalid_username(client, db_session):
    """Test retrieving a user without providing an ID or username."""

    response = client.get("/api/get/user/")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for missing user ID or username"

    response = client.get("/api/get/user/invaliduser!#")
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), "Expected 400 for invalid user ID or username format"
    assert (
        "detail" in response.json()
    ), "Response should contain validation error details"
