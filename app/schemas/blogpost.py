from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .tag import TagBase


class BlogpostBase(BaseModel):
    id: Optional[int]
    title: str
    slug: str
    tags: list[TagBase] = []
    banner: str
    content: str
    preview: str
    author_id: int
    created_at: datetime
    series_id: Optional[int]
    part_number: Optional[int]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class BlogpostShow(BlogpostBase):
    """Schema for showing blogpost details."""

    pass


class BlogpostCreate(BaseModel):
    """Schema for creating a new blogpost."""

    title: str
    slug: str
    tags: list[TagBase] = []
    banner: str
    content: str
    preview: str
    series_id: Optional[int] = None
    part_number: Optional[int] = None
    is_active: bool = True


class BlogpostUpdate(BaseModel):
    """Schema for updating an existing blogpost."""

    title: Optional[str] = None
    slug: Optional[str] = None
    tags: Optional[list[TagBase]] = None
    banner: Optional[str] = None
    content: Optional[str] = None
    preview: Optional[str] = None
    author_id: Optional[int] = None
    series_id: Optional[int] = None
    part_number: Optional[int] = None
    is_active: Optional[bool] = None
