from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.jwt import verify_access_token
from app.db.session import get_db
from app.models import User
from app.schemas import UserShow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserShow:
    try:
        payload = verify_access_token(token)
        user_id = payload.get("sub")
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserShow.model_validate(user)


def set_secure_cookie(response: JSONResponse, name: str, value: str) -> JSONResponse:
    """Set secure cookie in the response"""

    response.set_cookie(
        key=name,
        value=value,
        httponly=True,
        secure=not settings.IS_DEV,
        path="/",
        samesite="strict" if settings.IS_DEV else "none",
    )
    return response


def validate_refresh_token(
    refresh_token_payload: dict, access_token_payload: dict, fingerprint: str
) -> None:
    """Validate refresh token and access token against the request data"""
    if refresh_token_payload.get("fingerprint") != fingerprint:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Device ID mismatch. Please login again.",
        )

    sub = refresh_token_payload.get("sub")
    if not sub or access_token_payload.get("sub") != sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch. Please login again.",
        )
