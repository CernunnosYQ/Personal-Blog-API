from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models import User


def crud_get_user(
    db: Session, id: int | None = None, username: str | None = None
) -> User:
    """Fetch a single user by ID or username."""

    if id is not None:
        return db.query(User).filter_by(id=id).first()
    if username is not None:
        return db.query(User).filter_by(username=username).first()

    raise ValueError("Either id or username must be provided.")


def crud_create_user(user_data: dict, db: Session) -> User:
    """Create a new user in the database."""

    if crud_get_user(username=user_data.get("username"), db=db):
        raise ConflictError("Username already exists.")

    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def crud_update_user(id: int, user_data: dict, db: Session) -> User:
    """Update an existing user in the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise NotFoundError("User not found.")

    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def crud_update_user_password(id: int, password_data: dict, db: Session) -> dict:
    """Update the password of an existing user in the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise NotFoundError("User not found.")

    if user.password != password_data.get("old_password"):
        raise PermissionError("Old password is incorrect.")

    if user.password == password_data.get("new_password"):
        raise ValueError("New password must be different from the current password.")

    user.password = password_data.get("new_password")
    db.commit()
    return {"message": "Password updated successfully"}


def crud_delete_user(id: int, db: Session) -> dict:
    """Delete a user from the database."""

    user = crud_get_user(id=id, db=db)
    if not user:
        raise NotFoundError("User not found.")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
