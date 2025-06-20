from fastapi import APIRouter, status

from app.schemas import ResponseBase, TagCreate, TagShow, TagUpdate

router_tag = APIRouter(tags=["tag"])


@router_tag.get("/get/tags", response_model=ResponseBase[list[TagShow]])
async def get_tags() -> dict:
    """Get all tags"""

    return {"success": True, "data": []}


@router_tag.post(
    "/create/tag",
    response_model=ResponseBase[TagShow],
    status_code=status.HTTP_201_CREATED,
)
async def create_tag(tag: TagCreate) -> dict:
    """Create a new tag"""

    return {"success": True, "data": {}}


@router_tag.put("/update/tag/{id}", response_model=ResponseBase[TagShow])
async def update_tag(id: int, tag: TagUpdate) -> dict:
    """Update an existing tag"""

    return {"success": True, "data": {}}


@router_tag.get("/get/techs", response_model=ResponseBase[list[TagShow]])
async def get_techs() -> dict:
    """Get all tech tags"""

    return {"success": True, "data": []}


@router_tag.post(
    "/create/tech",
    response_model=ResponseBase[TagShow],
    status_code=status.HTTP_201_CREATED,
)
async def create_tech(tech: TagCreate) -> dict:
    """Create a new tech tag"""

    return {"success": True, "data": {}}


@router_tag.put("/update/tech/{id}", response_model=ResponseBase[TagShow])
async def update_tech(id: int, tech: TagUpdate) -> dict:
    """Update an existing tech tag"""

    return {"success": True, "data": {}}
