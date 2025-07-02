from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from tests.utils.schemas import UserExtended

new_data = {
    "username": "updateduser",
    "email": "updatedemail@gmail.com",
    "is_active": True,
}

new_password = "UpdatedPassword123"


def test_user_update_success(client: TestClient, test_user: UserExtended) -> None:
    """Test updating a user's information successfully."""

    user_id = test_user.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})
    response = client.put(f"/api/update/user/{user_id}", json=new_data)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json().get("data", {})
    assert response_data.get("username") == new_data["username"]
    assert response_data.get("email") == new_data["email"]


def test_user_update_not_found(client: TestClient, test_admin: UserExtended) -> None:
    """Test updating a user that does not exist."""

    token = test_admin.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    response = client.put("/api/get/user/")
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for missing user ID or username"

    response = client.put("/api/update/user/9999", json=new_data)
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), "Expected 404 for non-existent user"


def test_user_update_unauthorized(client: TestClient, test_user: UserExtended) -> None:
    """Test updating a user without authorization."""

    user_id = test_user.id

    client.headers.pop("Authorization", None)

    response = client.put(f"/api/update/user/{user_id}", json=new_data)
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), "Expected 401 Unauthorized for missing token"


def test_user_update_forbidden(
    client: TestClient, test_user: UserExtended, test_admin: UserExtended
) -> None:
    """Test updating a user without permission."""

    admin_id = test_admin.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    response = client.put(f"/api/update/user/{admin_id}", json=new_data)
    assert (
        response.status_code == status.HTTP_403_FORBIDDEN
    ), "Expected 403 Forbidden for unauthorized user update"


def test_update_user_raises_500(client: TestClient, test_user: UserExtended) -> None:
    """Test that an unexpected error raises a 500 status code."""

    user_id = test_user.id
    token = test_user.access_token

    client.headers.update({"Authorization": f"Bearer {token}"})

    with patch("app.api.user.crud_update_user") as mock_crud:
        mock_crud.side_effect = Exception("Unexpected error")

        response = client.put(f"/api/update/user/{user_id}", json=new_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while updating the user"}
