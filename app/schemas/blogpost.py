from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    project_id: Optional[int]
    created_at: datetime
    series_id: Optional[int]
    part_number: Optional[int]
    is_active: bool


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
    project_id: Optional[int] = None
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
    project_id: Optional[int] = None
    series_id: Optional[int] = None
    part_number: Optional[int] = None
    is_active: Optional[bool] = None
