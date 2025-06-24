from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
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
from app.schemas import ResponseBase, Token

router_auth = APIRouter(tags=["auth"])


@router_auth.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[Token],
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    fingerprint: str = Header(None, alias="x-Device-Fingerprint"),
    db: Session = Depends(get_db),
) -> dict:
    """Login a user and return an access token and a refresh token as a secure cookie"""

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

    refresh_token = create_refresh_token(sub=str(user.id), fingerprint=fingerprint)
    access_token = create_access_token(sub=str(user.id))

    response = JSONResponse(
        content={
            "success": True,
            "data": {"token_type": "bearer", "access_token": access_token},
            "message": "Login successful",
        }
    )

    response = set_secure_cookie(response, name="refresh_token", value=refresh_token)
    return response


@router_auth.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=ResponseBase[Token]
)
def refresh_token(
    request: Request,
    access_token: str | None = Header(None, alias="Authorization"),
    fingerprint: str = Header(None, alias="x-Device-Fingerprint"),
) -> dict:
    """Refresh user token"""

    refresh_token = request.cookies.get("refresh_token")
    access_token = access_token.split(" ")[1] if access_token else None

    if not refresh_token or not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token or access token",
        )

    try:
        refresh_token_payload = verify_access_token(refresh_token)
        access_token_payload = decode_expired_token(access_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    validate_refresh_token(refresh_token_payload, access_token_payload, fingerprint)

    new_access_token = create_access_token(sub=str(access_token_payload.get("sub")))

    return JSONResponse(
        content={
            "success": True,
            "data": {"token_type": "bearer", "access_token": new_access_token},
            "message": "Login successful",
        }
    )


@router_auth.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[None],
)
def logout_user() -> dict:
    """Logout a user by clearing cookies"""

    response = JSONResponse(
        content={"success": True, "data": None, "message": "Logout successful"}
    )
    response.delete_cookie("refresh_token", path="/")
    return response
