from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    id: Optional[int]
    name: str
    icon: str
    description: Optional[str] = None
