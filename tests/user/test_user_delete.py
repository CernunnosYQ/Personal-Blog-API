from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from tests.utils.schemas import UserExtended


def test_user_delete_success(client: TestClient, test_user: UserExtended) -> None:
    """Test deleting a user successfully."""

    user_id = test_user.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})
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


def test_user_delete_not_found(client: TestClient, test_admin: UserExtended) -> None:
    """Test deleting a user that does not exist."""

    token = test_admin.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    response = client.delete("/api/delete/user/9999")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user"


def test_delete_user_unauthorized(
    client: TestClient, test_user: UserExtended, test_admin: UserExtended
) -> None:
    """Test that a user cannot delete another user without admin rights."""

    admin_id = test_admin.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    response = client.delete(f"/api/delete/user/{admin_id}")
    assert (
        response.status_code == status.HTTP_403_FORBIDDEN
    ), "Expected 403 Forbidden for non-admin user trying to delete another user"


def test_delete_user_raises_500(client: TestClient, test_user: UserExtended) -> None:
    """Test that an unexpected error raises a 500 status code."""

    user_id = test_user.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    with patch("app.api.user.crud_delete_user") as mock_crud:
        mock_crud.side_effect = Exception("Unexpected error")

        response = client.delete(f"/api/delete/user/{user_id}")

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while deleting the user"}
