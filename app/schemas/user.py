from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from enums import UserRoles


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    role: UserRoles
    is_active: bool
