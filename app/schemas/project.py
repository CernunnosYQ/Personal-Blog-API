from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.enums import Tier
from .tag import TagBase


class ProjectBase(BaseModel):
    id: Optional[int]
    banner: str
    title: str
    oneliner: str
    author_id: int
    description: str
    techs: list[TagBase] = []
    blogpost_id: str
    preview_link: str
    github_link: str
    created_at: datetime
    last_updated: datetime
    tier: Tier
    is_active: bool

    class Config:
        orm_mode: True


class ProjectShow(ProjectBase):
    """Schema for showing project details."""

    pass


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    banner: str
    title: str
    oneliner: str
    description: str
    techs: list[TagBase] = []
    blogpost_id: str
    preview_link: str
    github_link: str
    tier: Tier
    is_active: bool


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    banner: Optional[str] = None
    title: Optional[str] = None
    oneliner: Optional[str] = None
    author_id: Optional[int] = None
    description: Optional[str] = None
    techs: list[TagBase] = []
    blogpost_id: Optional[str] = None
    preview_link: Optional[str] = None
    github_link: Optional[str] = None
    tier: Optional[Tier] = None
    is_active: Optional[bool] = None
