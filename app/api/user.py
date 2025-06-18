from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import re

from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.schemas import (
    ResponseBase,
    UserShow,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
)
from app.crud import (
    crud_get_user,
    crud_create_user,
    crud_update_user,
    crud_update_user_password,
    crud_delete_user,
)

username_pattern = r"^[a-zA-Z0-9_]{3,20}$"
router_user = APIRouter(tags=["user"])


@router_user.get("/get/user/{user_id}", response_model=ResponseBase[UserShow])
async def get_user(user_id, db: Session = Depends(get_db)):
    """Get an user by id or username"""

    if user_id.isdigit():
        user = crud_get_user(id=int(user_id), db=db)
    else:
        if not re.fullmatch(username_pattern, user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username format",
            )
        user = crud_get_user(username=user_id, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"success": True, "message": "User found", "data": user}


@router_user.post(
    "/create/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[UserShow],
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""

    user_data = user.model_dump(exclude={"password2"})

    try:
        new_user = crud_create_user(user_data=user_data, db=db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user",
        )

    return {"success": True, "message": "User created", "data": new_user}


@router_user.put("/update/user/{id}", response_model=ResponseBase[UserShow])
async def update_user(id, user: UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user"""

    user = user.model_dump(exclude_unset=True)

    try:
        updated_user = crud_update_user(id=id, user_data=user, db=db)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user",
        )

    return {"success": True, "message": "User updated", "data": updated_user}


@router_user.put(
    "/update/password/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
async def update_password(
    id: int, user_password: UserPasswordUpdate, db: Session = Depends(get_db)
):
    """Update an existing user's password"""

    try:
        response = crud_update_user_password(
            id=id,
            password_data=user_password.model_dump(exclude={"new_password2"}),
            db=db,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the password" + str(e),
        )

    return {"success": True, "message": response["message"], "data": None}


@router_user.delete(
    "/delete/user/{id}",
    status_code=status.HTTP_200_OK,
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete a user"""

    try:
        response = crud_delete_user(id=id, db=db)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )

    return {"success": True, "message": response["message"], "data": None}
