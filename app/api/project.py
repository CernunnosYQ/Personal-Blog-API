from fastapi import APIRouter, status

from app.schemas import ProjectCreate, ProjectShow, ProjectUpdate, ResponseBase

router_project = APIRouter(tags=["project"])


@router_project.get("/get/projects", response_model=ResponseBase[list[ProjectShow]])
async def get_projects() -> dict:
    """Get all projects"""

    return {"success": True, "data": []}


@router_project.get(
    "/get/projects/{tech}", response_model=ResponseBase[list[ProjectShow]]
)
async def get_projects_by_tech(tech: str = "all") -> dict:
    """Get all projects by tech tag"""

    return {"success": True, "data": []}


@router_project.get("/get/project/{id}", response_model=ResponseBase[ProjectShow])
async def get_project(id: int) -> dict:
    """Get one project by id"""

    return {"success": True, "data": {}}


@router_project.post(
    "/create/project",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBase[ProjectShow],
)
async def create_project(project: ProjectCreate) -> dict:
    """Create a new project"""

    return {"success": True, "data": {}}


@router_project.put("/update/project/{id}", response_model=ResponseBase[ProjectShow])
async def update_project(id: int, project: ProjectUpdate) -> dict:
    """Update an existing project"""

    return {"success": True, "data": {}}


@router_project.delete("/delete/project/{id}", response_model=ResponseBase[None])
async def delete_project(id: int) -> dict:
    """Delete a project"""

    return {"success": True, "data": None}
