from sqlalchemy import Table, Column, Integer, ForeignKey
from core.db.base import Base

blogpost_tags = Table(
    "blogpost_tags",
    Base.metadata,
    Column("blogpost_id", Integer, ForeignKey("blogposts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

project_techs = Table(
    "project_techs",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("tech_id", Integer, ForeignKey("techs.id"), primary_key=True),
)
