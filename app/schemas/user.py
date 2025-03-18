# Temporal schema for user
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_active: bool
