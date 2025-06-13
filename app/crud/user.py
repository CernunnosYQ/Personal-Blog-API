from sqlalchemy.orm import Session
from app.models import User

from app.schemas import UserCreate, UserUpdate


def crud_get_user(id: int = None, username: str = None, db: Session = None):
    """Fetch a single user by ID or username."""

    if not db:
        raise ValueError("Database session is required.")
    if not (id or username):
        raise ValueError("Either id or username must be provided.")
    if id is not None:
        return db.query(User).filter_by(id=id).first()
    if username is not None:
        return db.query(User).filter_by(username=username).first()


def crud_create_user(user_data: dict, db: Session = None):
    """Create a new user in the database."""
    if not db:
        raise ValueError("Database session is required.")

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
