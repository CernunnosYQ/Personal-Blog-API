from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    id: Optional[int]
    name: str
    icon: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


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
