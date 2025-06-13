from fastapi import APIRouter, status
from app.schemas import ResponseBase, ProjectShow, ProjectCreate, ProjectUpdate

router_project = APIRouter(tags=["project"])


@router_project.get("/get/projects", response_model=ResponseBase[list[ProjectShow]])
async def get_projects():
    """Get all projects"""

    return {"success": True, "data": []}


@router_project.get(
    "/get/projects/{tech}", response_model=ResponseBase[list[ProjectShow]]
)
async def get_projects(tech: str = "all"):
    """Get all projects by tech tag"""

    return {"success": True, "data": []}


@router_project.get("/get/project/{id}", response_model=ResponseBase[ProjectShow])
async def get_project(id: int):
    """Get one project by id"""

    return {"success": True, "data": {}}


@router_project.post(
    "/create/project",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[ProjectShow],
)
async def create_project(pproject: ProjectCreate):
    """Create a new project"""

    return {"success": True, "data": {}}


@router_project.put("/update/project/{id}", response_model=ResponseBase[ProjectShow])
async def update_project(id: int, project: ProjectUpdate):
    """Update an existing project"""

    return {"success": True, "data": {}}


@router_project.delete("/delete/project/{id}", response_model=ResponseBase[None])
async def delete_project(id: int):
    """Delete a project"""

    return {"success": True, "data": None}
