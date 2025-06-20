from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas import ResponseBase
from app.utils.jwt import create_access_token, create_refresh_token

router_auth = APIRouter(tags=["auth"])


@router_auth.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    """Login a user  and create new access and refresh tokens as secure cookies"""

    user = (
        db.query(User)
        .filter(
            and_(
                User.is_active is True,
                or_(
                    User.username == form_data.username,
                    User.email == form_data.username,
                ),
            )
        )
        .first()
    )

    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    client_ip = request.headers.get("x-forwarded-for") or request.client.host
    user_agent = request.headers.get("user-agent")

    refresh_token = create_refresh_token(
        data={"sub": user.id, "ip": client_ip, "user_agent": user_agent}
    )
    access_token = create_access_token(data={"sub": user.id})

    response = JSONResponse(
        content={"success": True, "data": None, "message": "Login successful"}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return response


@router_auth.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=ResponseBase[None]
)
def refresh_token(user_data: dict, db: Session = Depends(get_db)) -> dict:
    """Refresh user token"""

    return {"success": True, "data": {}}


@router_auth.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
def logout_user(db: Session = Depends(get_db)) -> dict:
    """Logout a user"""

    return {"success": True, "data": None}
