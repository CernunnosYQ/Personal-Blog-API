from fastapi import APIRouter, status
from app.schemas import ResponseBase, BlogpostShow, BlogpostCreate, BlogpostUpdate


router_blog = APIRouter(tags=["blogpost"])


@router_blog.get("/get/blogposts", response_model=ResponseBase[list[BlogpostShow]])
async def get_blogposts():
    """Get all blogposts"""

    return {"success": True, "data": []}


@router_blog.get(
    "/get/blogposts/{tag}", response_model=ResponseBase[list[BlogpostShow]]
)
async def get_blogposts(tag: str = "all"):
    """Get all blogposts by tag"""

    return {"success": True, "data": []}


@router_blog.get("/get/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost(id: int):
    """Get one blogpost by id"""

    return {"success": True, "data": {}}


@router_blog.get("/get/blogpost/{slug}", response_model=ResponseBase[BlogpostShow])
async def get_blogpost(slug: str):
    """Get one blogpost by slug"""

    return {"success": True, "data": {}}


@router_blog.post(
    "/create/blogpost",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[BlogpostShow],
)
async def create_blogpost(blogpost: BlogpostCreate):
    """Create a new blogpost"""

    return {"success": True, "data": {}}


@router_blog.put("/update/blogpost/{id}", response_model=ResponseBase[BlogpostShow])
async def update_blogpost(id: int, blogpost: BlogpostUpdate):
    """Update an existing blogpost"""

    return {"success": True, "data": {}}


@router_blog.delete("/delete/blogpost/{id}", response_model=ResponseBase[None])
async def delete_blogpost(id: int):
    """Delete a blogpost"""

    return {"success": True, "data": None}
