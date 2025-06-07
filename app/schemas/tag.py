from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    id: Optional[int]
    name: str
    icon: str
    description: Optional[str] = None


class TagShow(TagBase):
    """Schema for showing tag details."""

    pass


class TagCreate(BaseModel):
    """Schema for creating a new tag."""

    name: str
    icon: str
    description: Optional[str] = None


class TagUpdate(BaseModel):
    """Schema for updating an existing tag."""

    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
