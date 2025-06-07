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
