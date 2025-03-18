from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Tier(str):
    allowed_tiers = {"S", "A", "B", "C", "D"}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if value not in cls.allowed_tiers:
            raise ValueError(f"Tier must be one of {cls.allowed_tiers}")
        return value


class Project(BaseModel):
    id: Optional[int]
    banner: str
    title: str
    project_type: str
    author_id: int
    description: str
    tags: list[str]
    blogpost_id: str
    preview_link: str
    github_link: str
    created_at: datetime
    last_updated: datetime
    tier: Tier
    is_active: bool

    class Config:
        orm_mode: True


# export type TProject = {
#     id: number
#     banner: string
#     title: string
#     type: string
#     author: string
#     description: string
#     tags: string[]
#     blogpost_id: number
#     preview_link: string
#     github_link: string
#     created_at: Date
#     tier: 'S' | 'A' | 'B' | 'C' | 'F'
#     is_active: boolean
# }
