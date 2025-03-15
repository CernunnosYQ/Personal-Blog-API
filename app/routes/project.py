from fastapi import APIRouter, status

router_project = APIRouter(tags=["project"])


@router_project.get("/get/projects")
async def get_projects():
    """Get all projects"""

    return {"success": True, "data": []}


@router_project.get("/get/projects/{tech}")
async def get_projects(tech: str = "all"):
    """Get all projects by tech tag"""

    return {"success": True, "data": []}


@router_project.get("/get/project/{id}")
async def get_project(id: int):
    """Get one project by id"""

    return {"success": True, "data": {}}


@router_project.post("/create/project", status_code=status.HTTP_201_CREATED)
async def create_project():
    """Create a new project"""

    return {"success": True, "data": {}}


@router_project.put("/update/project/{id}")
async def update_project(id: int):
    """Update an existing project"""

    return {"success": True, "data": {}}


@router_project.delete("/delete/project/{id}")
async def delete_project(id: int):
    """Delete a project"""

    return {"success": True, "data": {}}
