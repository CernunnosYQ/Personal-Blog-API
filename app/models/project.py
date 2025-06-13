from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base
from app.core.enums import Tier
from .association_tables import project_techs


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    banner = Column(String, nullable=True)
    title = Column(String, unique=True, index=True, nullable=False)
    oneliner = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    techs = relationship("Tech", secondary=project_techs, back_populates="projects")
    blogpost_id = Column(Integer, ForeignKey("blogposts.id"), nullable=True)
    preview_link = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_update = Column(DateTime, default=datetime.now(timezone.utc))
    tier = Column(Enum(Tier), default=Tier.D, nullable=False)
    is_active = Column(Boolean, default=True)

    author = relationship("User", back_populates="projects")
    blogpost = relationship("Blogpost", back_populates="project", uselist=False)

    def __repr__(self):
        return (
            f"<Project(id={self.id}, title={self.title}, author_id={self.author_id})>"
        )
