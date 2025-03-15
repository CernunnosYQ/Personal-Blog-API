from fastapi import APIRouter, status


router_user = APIRouter(tags=["user"])


@router_user.get("/get/user/{id}")
async def get_user(id: int):
    """Get one user by id"""

    return {"success": True, "data": {}}


@router_user.get("/get/user/{username}")
async def get_user(username: str):
    """Get one user by username"""

    return {"success": True, "data": {}}


@router_user.post("/create/user", status_code=status.HTTP_201_CREATED)
async def create_user():
    """Create a new user"""

    return {"success": True, "data": {}}


@router_user.put("/update/user/{id}")
async def update_user(id: int):
    """Update an existing user"""

    return {"success": True, "data": {}}


@router_user.put("/update/password/{id}")
async def update_password(id: int):
    """Update an existing user's password"""

    return {"success": True, "data": {}}


@router_user.delete("/delete/user/{id}")
async def delete_user(id: int):
    """Delete a user"""

    return {"success": True, "data": {}}
