from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.auth import set_secure_cookie, validate_refresh_token
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_expired_token,
    verify_access_token,
)
from app.crud import crud_get_user
from app.db.session import get_db
from app.schemas import ResponseBase

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

    user = crud_get_user(
        db=db,
        username=form_data.username,
        only_active=True,
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

    response = set_secure_cookie(response, name="refresh_token", value=refresh_token)
    response = set_secure_cookie(response, name="access_token", value=access_token)

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

    validate_refresh_token(refresh_token_payload, access_token_payload, request)

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

    response = set_secure_cookie(response, name="access_token", value=new_access_token)

    return response


@router_auth.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
def logout_user(db: Session = Depends(get_db)) -> dict:
    """Logout a user by clearing cookies"""

    response = JSONResponse(
        content={"success": True, "data": None, "message": "Logout successful"}
    )
    response.delete_cookie("refresh_token", path="/")
    response.delete_cookie("access_token", path="/")
    return response
