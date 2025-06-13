from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import (
    ResponseBase,
    UserShow,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
)
from app.crud import crud_get_user, crud_create_user


router_user = APIRouter(tags=["user"])


@router_user.get("/get/user/{user_id}", response_model=ResponseBase[UserShow])
async def get_user(user_id, db: Session = Depends(get_db)):
    """Get an user by id or username"""

    if not user_id:
        return {
            "success": False,
            "message": "User ID or username is required",
            "data": None,
        }

    if user_id.isdigit():
        user = crud_get_user(id=int(user_id), db=db)
    else:
        user = crud_get_user(username=user_id, db=db)

    return {"success": True, "message": "User found", "data": user}


@router_user.post(
    "/create/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[UserShow],
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    user_data = user.model_dump(exclude={"password2"})

    new_user = crud_create_user(user_data=user_data, db=db)
    if not new_user:
        return {"success": False, "message": "User creation failed", "data": None}

    return {"success": True, "message": "User created", "data": new_user}


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
