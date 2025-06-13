from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.core.enums import UserRoles


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, default=UserRoles.USER, nullable=False)
    is_active = Column(Boolean, default=True)

    blogposts = relationship(
        "Blogpost", back_populates="author", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="author", cascade="all, delete-orphan"
    )
