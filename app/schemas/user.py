from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, constr, model_validator

from app.core.enums import UserRoles
from app.core.password import hash_password


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    role: UserRoles
    is_active: bool


class UserShow(BaseModel):
    """Schema for showing user details"""

    id: int
    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    username: str
    email: str
    password: Annotated[
        str,
        constr(
            min_length=8,
            strip_whitespace=True,
            pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$",
        ),
    ]
    password2: str
    is_active: bool = True

    @model_validator(mode="after")
    def validate_passwords(self) -> "UserCreate":
        if self.password != self.password2:
            raise ValueError("Passwords do not match")

        self.password = hash_password(self.password)
        return self


class UserUpdate(BaseModel):
    """Schema for updating an existing user"""

    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoles] = None
    is_active: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    """Schema for updating a user's password"""

    new_password: Annotated[
        str,
        constr(
            min_length=8, pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$"
        ),
    ]
    new_password2: str
    old_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> "UserPasswordUpdate":
        if self.new_password != self.new_password2:
            raise ValueError("Passwords do not match")
        return self
