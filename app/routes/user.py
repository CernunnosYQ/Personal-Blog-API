from fastapi import APIRouter, status

from app.schemas import (
    ResponseBase,
    UserShow,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
)


router_user = APIRouter(tags=["user"])


@router_user.get("/get/user/{id}", response_model=ResponseBase[UserShow])
async def get_user(id: int):
    """Get one user by id"""

    return {"success": True, "message": "User found", "data": {}}


@router_user.get("/get/user/{username}", response_model=ResponseBase[UserShow])
async def get_user(username: str):
    """Get one user by username"""

    return {"success": True, "message": "User found", "data": {}}


@router_user.post(
    "/create/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[UserShow],
)
async def create_user(user: UserCreate):
    """Create a new user"""

    return {"success": True, "message": "User created", "data": {}}


@router_user.put("/update/user/{id}", response_model=ResponseBase[UserShow])
async def update_user(id: int, user: UserUpdate):
    """Update an existing user"""

    return {"success": True, "message": "User updated", "data": {}}


@router_user.put(
    "/update/password/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
async def update_password(id: int, user_password: UserPasswordUpdate):
    """Update an existing user's password"""

    return {"success": True, "message": "Password updated", "data": {}}


@router_user.delete(
    "/delete/user/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(id: int):
    """Delete a user"""
