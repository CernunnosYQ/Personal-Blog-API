from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BlogpostBase(BaseModel):
    id: Optional[int]
    title: str
    slug: str
    tags: list[str]
    banner: str
    content: str
    preview: str
    author_id: int
    created_at: datetime
    previous_id: Optional[int]
    next_id: Optional[int]
    is_active: bool
