import pytest

from fastapi import status
from unittest.mock import patch


def test_user_delete_success(client, db_session, test_user):
    """Test deleting a user successfully."""

    user_id = test_user.id
    response = client.delete(f"/api/delete/user/{user_id}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), "Expected successful user deletion"

    response_data = response.json()
    assert (
        response_data.get("success") is True
    ), "Expected success response for user deletion"

    # Verify the user is actually deleted
    response = client.get(f"/api/get/user/{user_id}")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for deleted user"


def test_user_delete_not_found(client, db_session):
    """Test deleting a user that does not exist."""

    response = client.delete("/api/delete/user/9999")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user"


def test_delete_user_raises_500(client, test_user):
    """Test that an unexpected error raises a 500 status code."""

    user_id = test_user.id

    with patch("app.api.user.crud_delete_user") as mock_crud:
        mock_crud.side_effect = Exception("Unexpected error")

        response = client.delete(f"/api/delete/user/{user_id}")

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while deleting the user"}
