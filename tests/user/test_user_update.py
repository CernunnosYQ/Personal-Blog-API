import pytest

from fastapi import status
from unittest.mock import patch

new_data = {
    "username": "updateduser",
    "email": "updatedemail@gmail.com",
    "is_active": True,
}

new_password = "UpdatedPassword123"


def test_user_update_success(client, db_session, test_user):
    """Test updating a user's information successfully."""

    user_id = test_user.id
    response = client.put(f"/api/update/user/{user_id}", json=new_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json().get("data", {})
    assert response_data.get("username") == new_data["username"]
    assert response_data.get("email") == new_data["email"]


def test_user_update_not_found(client, db_session):
    """Test updating a user that does not exist."""

    response = client.put("/api/get/user/")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for missing user ID or username"

    response = client.put("/api/update/user/9999", json=new_data)
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user"


def test_update_user_raises_500(client, test_user):
    """Test that an unexpected error raises a 500 status code."""

    user_id = test_user.id

    with patch("app.api.user.crud_update_user") as mock_crud:
        mock_crud.side_effect = Exception("Unexpected error")

        response = client.put(f"/api/update/user/{user_id}", json=new_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while updating the user"}
