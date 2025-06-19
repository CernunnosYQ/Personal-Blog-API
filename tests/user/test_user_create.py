import pytest

from fastapi import status
from unittest.mock import patch


user_example = {
    "username": "testuser",
    "email": "test@gmail.com",
    "secure_password": "SecurePassword123",
    "unsecure_password": "testpassword",
    "is_active": True,
}


def test_create_user_success(client):
    user_data = {
        "username": user_example["username"],
        "email": user_example["email"],
        "password": user_example["secure_password"],
        "password2": user_example["secure_password"],
        "is_active": user_example["is_active"],
    }

    response = client.post("/api/create/user/", json=user_data)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Expected successful user creation"
    data = response.json().get("data", {})
    assert (
        data["username"] == user_example["username"]
    ), "Username should match the input"
    assert data["email"] == user_example["email"], "Email should match the input"
    assert "id" in data, "Response should contain user ID"


def test_create_user_missing_fields(client):
    user_data = {
        "username": user_example["username"],
        "password": user_example["secure_password"],
        "password2": user_example["secure_password"],
        "is_active": user_example["is_active"],
    }

    response = client.post("/api/create/user/", json=user_data)
    assert response.status_code == 422, "Expected validation error for missing fields"


def test_create_user_password_missmatch(client):
    user_data = {
        "username": user_example["username"],
        "email": user_example["email"],
        "password": user_example["secure_password"],
        "password2": user_example["unsecure_password"],
        "is_active": user_example["is_active"],
    }

    response = client.post("/api/create/user/", json=user_data)
    assert (
        response.status_code == 422
    ), "Expected validation error for password mismatch"


def test_create_user_already_exists(client):
    user_data = {
        "username": user_example["username"],
        "email": user_example["email"],
        "password": user_example["secure_password"],
        "password2": user_example["secure_password"],
        "is_active": user_example["is_active"],
    }

    client.post("/api/create/user/", json=user_data)

    response = client.post("/api/create/user/", json=user_data)
    assert response.status_code == 409, "Expected 409 Conflict for user already exists"


def test_create_user_raises_500(client):
    user_data = {
        "username": user_example["username"],
        "email": user_example["email"],
        "password": user_example["secure_password"],
        "password2": user_example["secure_password"],
        "is_active": user_example["is_active"],
    }

    with patch("app.api.user.crud_create_user") as mock_crud:
        mock_crud.side_effect = Exception("Unexpected error")

        response = client.post("/api/create/user", json=user_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while creating the user"}
