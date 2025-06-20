from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base

from .association_tables import blogpost_tags


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)

    blogposts = relationship(
        "Blogpost", back_populates="series", cascade="all, delete-orphan"
    )


class Blogpost(Base):
    __tablename__ = "blogposts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    banner = Column(String, nullable=True)
    content = Column(String, nullable=False)
    preview = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)
    part_number = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    author = relationship("User", back_populates="blogposts")
    tags = relationship("Tag", secondary=blogpost_tags, back_populates="blogposts")
    project = relationship("Project", back_populates="blogpost")
    series = relationship("Series", back_populates="blogposts")

    def __repr__(self) -> str:
        return (
            f"<Blogpost(id={self.id}, title={self.title}, author_id={self.author_id}, "
            f"slug={self.slug}, created_at={self.created_at})>"
        )
