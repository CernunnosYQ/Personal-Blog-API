from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from enums import Tier
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
