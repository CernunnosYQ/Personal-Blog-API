from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas import ResponseBase
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_expired_token,
    verify_access_token,
)

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
                User.is_active == True,  # noqa: E712
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
        data={"sub": str(user.id), "ip": client_ip, "user_agent": user_agent}
    )
    access_token = create_access_token(data={"sub": str(user.id)})

    response = JSONResponse(
        content={"success": True, "data": None, "message": "Login successful"}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        path="/",
        samesite="strict",
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        path="/",
        samesite="strict",
    )

    return response


@router_auth.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=ResponseBase[None]
)
def refresh_token(request: Request, db: Session = Depends(get_db)) -> dict:
    """Refresh user token"""

    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")

    if not refresh_token or not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing. Please login again.",
        )

    try:
        refresh_token_payload = verify_access_token(refresh_token)
        access_token_payload = decode_expired_token(access_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if refresh_token_payload.get("ip") != request.client.host:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="IP address mismatch. Please login again.",
        )

    if refresh_token_payload.get("user_agent") != request.headers.get("user-agent"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User agent mismatch. Please login again.",
        )

    sub = refresh_token_payload.get("sub")
    if not sub or access_token_payload.get("sub") != sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch. Please login again.",
        )

    new_access_token = create_access_token(
        data={"sub": access_token_payload.get("sub")}
    )

    response = JSONResponse(
        content={
            "success": True,
            "data": None,
            "message": "Token refreshed successfully",
        }
    )

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        path="/",
        samesite="strict",
    )

    return response


@router_auth.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
def logout_user(db: Session = Depends(get_db)) -> dict:
    """Logout a user"""

    response = JSONResponse(
        content={"success": True, "data": None, "message": "Logout successful"}
    )
    response.delete_cookie("refresh_token", path="/")
    response.delete_cookie("access_token", path="/")
    return response
