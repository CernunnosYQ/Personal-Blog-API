from pydantic import BaseModel
from typing import Optional

from app.core.enums import UserRoles


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    role: UserRoles
    is_active: bool


class UserShow(BaseModel):
    """Schema for showing user details"""

    username: str
    email: str
    is_active: bool


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    username: str
    email: str
    password: str
    password2: str
    is_active: bool = True


class UserUpdate(BaseModel):
    """Schema for updating an existing user"""

    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoles] = None
    is_active: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    """Schema for updating a user's password"""

    new_password: str
    new_password2: str
    old_password: str
