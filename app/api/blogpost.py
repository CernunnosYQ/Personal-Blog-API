from fastapi import APIRouter, status

from app.schemas import BlogpostCreate, BlogpostShow, BlogpostUpdate, ResponseBase

router_blog = APIRouter(tags=["blogpost"])


@router_blog.get("/get/blogposts", response_model=ResponseBase[list[BlogpostShow]])
async def get_blogposts() -> dict:
    """Get all blogposts"""

    return {"success": True, "data": []}


@router_blog.get(
    "/get/blogposts/{tag}", response_model=ResponseBase[list[BlogpostShow]]
)
async def get_blogposts_by_tag(tag: str = "all") -> dict:
    """Get all blogposts by tag"""

    return {"success": True, "data": []}


@router_blog.get("/get/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost_by_id(id: int) -> dict:
    """Get one blogpost by id"""

    return {"success": True, "data": {}}


@router_blog.get("/get/blogpost/{slug}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost_by_slug(slug: str) -> dict:
    """Get one blogpost by slug"""

    return {"success": True, "data": {}}


@router_blog.post(
    "/create/blogpost",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[BlogpostShow],
)
async def create_blogpost(blogpost: BlogpostCreate) -> dict:
    """Create a new blogpost"""

    return {"success": True, "data": {}}


@router_blog.put("/update/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def update_blogpost(id: int, blogpost: BlogpostUpdate) -> dict:
    """Update an existing blogpost"""

    return {"success": True, "data": {}}


@router_blog.delete("/delete/blogpost/{id}", response_model=ResponseBase[None])
async def delete_blogpost(id: int) -> dict:
    """Delete a blogpost"""

    return {"success": True, "data": None}
