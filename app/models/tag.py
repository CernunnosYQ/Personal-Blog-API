from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.db.base import Base

from .association_tables import blogpost_tags, project_techs


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

    blogposts = relationship("Blogpost", secondary=blogpost_tags, back_populates="tags")


class Tech(Base):
    __tablename__ = "techs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    icon = Column(String, nullable=True)
    description = Column(String, nullable=True)

    projects = relationship("Project", secondary=project_techs, back_populates="techs")
