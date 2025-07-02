from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.exceptions import ConflictError, NotFoundError
from app.crud import (
    crud_create_blogpost,
    crud_delete_blogpost,
    crud_get_blogpost,
    crud_get_blogposts,
    crud_update_blogpost,
    is_author_of_blogpost,
)
from app.db.session import get_db
from app.schemas import (
    BlogpostCreate,
    BlogpostShow,
    BlogpostUpdate,
    ResponseBase,
    UserShow,
)

router_blog = APIRouter(tags=["blogpost"])


@router_blog.get("/get/blogposts", response_model=ResponseBase[list[BlogpostShow]])
async def get_blogposts(db: Session = Depends(get_db)) -> dict:
    """Get all blogposts"""

    data = crud_get_blogposts(db=db, tag="all", only_active=True)
    return {"success": True, "data": data}


@router_blog.get(
    "/get/blogposts/{tag}", response_model=ResponseBase[list[BlogpostShow]]
)
async def get_blogposts_by_tag(tag: str = "all", db: Session = Depends(get_db)) -> dict:
    """Get all blogposts by tag"""

    data = crud_get_blogposts(db=db, tag=tag, only_active=True)
    return {"success": True, "data": data}


@router_blog.get("/get/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    """Get one blogpost by id"""

    data = crud_get_blogpost(db=db, id=id)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blogpost not found",
        )

    return {"success": True, "data": data}


@router_blog.get("/get/blogpost/{id_slug}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost_by_slug(
    id_slug: str = Path(..., pattern=r"^[a-zA-Z0-9_]+$"), db: Session = Depends(get_db)
) -> dict:
    """Get one blogpost by slug"""

    if id_slug.isdigit():
        data = crud_get_blogpost(db=db, id=int(id_slug))
    else:
        data = crud_get_blogpost(db=db, slug=id_slug)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blogpost not found",
        )

    return {"success": True, "data": data}


@router_blog.post(
    "/create/blogpost",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[BlogpostShow],
)
async def create_blogpost(
    blogpost: BlogpostCreate, db: Session = Depends(get_db)
) -> dict:
    """Create a new blogpost"""

    try:
        new_blogpost = crud_create_blogpost(blogpost_data=blogpost, db=db)
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the blogpost",
        )

    return {"success": True, "data": new_blogpost}


@router_blog.put("/update/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def update_blogpost(
    id: int,
    new_data: BlogpostUpdate,
    db: Session = Depends(get_db),
    current_user: UserShow = Depends(get_current_user),
) -> dict:
    """Update an existing blogpost"""

    if (
        is_author_of_blogpost(db=db, blogpost_id=id, user_id=current_user.id)
        and not current_user.role.is_admin()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this blogpost",
        )

    blogpost_data = new_data.model_dump(exclude_unset=True)

    try:
        updated_blogpost = crud_update_blogpost(
            id=id, blogpost_data=blogpost_data, db=db
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return {"success": True, "data": updated_blogpost}


@router_blog.delete("/delete/blogpost/{id}", response_model=ResponseBase[None])
async def delete_blogpost(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserShow = Depends(get_current_user),
) -> dict:
    """Delete a blogpost"""

    if (
        is_author_of_blogpost(db=db, blogpost_id=id, user_id=current_user.id)
        and not current_user.role.is_admin()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this blogpost",
        )

    try:
        crud_delete_blogpost(id=id, db=db)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return {"success": True, "data": None}
