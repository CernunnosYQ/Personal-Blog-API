from fastapi import APIRouter, status


router_blog = APIRouter(tags=["blogpost"])


@router_blog.get("/get/blogposts")
async def get_blogposts():
    """Get all blogposts"""

    return {"success": True, "data": []}


@router_blog.get("/get/blogposts/{tag}")
async def get_blogposts(tag: str = "all"):
    """Get all blogposts by tag"""

    return {"success": True, "data": []}


@router_blog.get("/get/blogpost/{id}")
async def get_blogpost(id: int):
    """Get one blogpost by id"""

    return {"success": True, "data": {}}


@router_blog.get("/get/blogpost/{slug}")
async def get_blogpost(slug: str):
    """Get one blogpost by slug"""

    return {"success": True, "data": {}}


@router_blog.post("/create/blogpost", status_code=status.HTTP_201_CREATED)
async def create_blogpost():
    """Create a new blogpost"""

    return {"success": True, "data": {}}


@router_blog.put("/update/blogpost/{id}")
async def update_blogpost(id: int):
    """Update an existing blogpost"""

    return {"success": True, "data": {}}


@router_blog.delete("/delete/blogpost/{id}")
async def delete_blogpost(id: int):
    """Delete a blogpost"""

    return {"success": True, "data": {}}
