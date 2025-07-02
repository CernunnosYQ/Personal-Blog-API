from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models import Blogpost


def is_author_of_blogpost(db: Session, blogpost_id: int, user_id: int) -> bool:
    """Check if the user is the author of the blogpost."""

    return db.query(
        db.query(Blogpost)
        .filter(Blogpost.id == blogpost_id, Blogpost.author_id == user_id)
        .exists()
    ).scalar()


def crud_get_blogposts(
    db: Session, tag: str = "all", only_active: bool = True
) -> list[Blogpost]:
    """Fetch all blogposts, optionally filtered by tag."""
    query = db.query(Blogpost)

    if tag != "all":
        query = query.filter(Blogpost.tags.any(name=tag))

    if only_active:
        query = query.filter(Blogpost.is_active == True)  # noqa: E712

    return query.all()


def crud_get_blogpost(
    db: Session, id: int | None = None, slug: str | None = None
) -> Blogpost:
    """Fetch a single blogpost by ID or slug."""
    if id is not None:
        return db.query(Blogpost).filter_by(id=id).first()

    if slug is not None:
        return db.query(Blogpost).filter_by(slug=slug).first()

    raise ValueError("Either id or slug must be provided.")


def crud_create_blogpost(blogpost_data: dict, db: Session) -> Blogpost:
    """Create a new blogpost in the database."""
    if crud_get_blogpost(slug=blogpost_data.get("slug"), db=db):
        raise ConflictError("Blogpost with this slug already exists.")

    new_blogpost = Blogpost(**blogpost_data)
    db.add(new_blogpost)
    db.commit()
    db.refresh(new_blogpost)
    return new_blogpost


def crud_update_blogpost(id: int, blogpost_data: dict, db: Session) -> Blogpost:
    """Update an existing blogpost in the database."""
    blogpost = crud_get_blogpost(id=id, db=db)
    if not blogpost:
        raise NotFoundError("Blogpost not found.")

    for key, value in blogpost_data.items():
        setattr(blogpost, key, value)

    db.commit()
    db.refresh(blogpost)
    return blogpost


def crud_delete_blogpost(id: int, db: Session) -> None:
    """Delete a blogpost from the database."""
    blogpost = crud_get_blogpost(id=id, db=db)
    if not blogpost:
        raise NotFoundError("Blogpost not found.")

    db.delete(blogpost)
    db.commit()
    return None
