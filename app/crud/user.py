from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models import User

from app.schemas import UserCreate, UserUpdate, UserPasswordUpdate


def crud_get_user(id: int = None, username: str = None, db: Session = None):
    """Fetch a single user by ID or username."""

    if id is not None:
        return db.query(User).filter_by(id=id).first()
    if username is not None:
        return db.query(User).filter_by(username=username).first()

    raise ValueError("Either id or username must be provided.")


def crud_create_user(user_data: dict, db: Session = None):
    """Create a new user in the database."""

    if crud_get_user(username=user_data.get("username"), db=db):
        raise ValueError("Username already exists.")

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def crud_update_user(id: int, user_data: dict, db: Session = None):
    """Update an existing user in the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise NotFoundError("User not found.")

    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def crud_update_user_password(id: int, password_data: dict, db: Session = None):
    """Update the password of an existing user in the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise ValueError("User not found.")

    if user.password != password_data.get("old_password"):
        raise PermissionError("Old password is incorrect.")

    if user.password == password_data.get("new_password"):
        raise ValueError("New password must be different from the current password.")

    user.password = password_data.get("new_password")
    db.commit()
    return {"message": "Password updated successfully"}


def crud_delete_user(id: int, db: Session = None):
    """Delete a user from the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise NotFoundError("User not found.")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
