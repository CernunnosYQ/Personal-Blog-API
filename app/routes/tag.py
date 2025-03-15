from fastapi import APIRouter, status

router_tag = APIRouter(tags=["tag"])


@router_tag.get("/get/tags")
async def get_tags():
    """Get all tags (for blogposts)"""

    return {"success": True, "data": []}


@router_tag.get("/get/tech-tags")
async def get_tech_tags():
    """Get all tech tags (for projects)"""

    return {"success": True, "data": []}
