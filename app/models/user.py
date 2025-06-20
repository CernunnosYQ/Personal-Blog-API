from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.core.enums import UserRoles
from app.db.base import Base
from app.utils.hashing import verify_password


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoles), default=UserRoles.USER, nullable=False)
    is_active = Column(Boolean, default=True)

    blogposts = relationship(
        "Blogpost", back_populates="author", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="author", cascade="all, delete-orphan"
    )

    def verify_password(self, password: str) -> bool:
        """Verify the user's password."""
        return verify_password(password, self.password)
