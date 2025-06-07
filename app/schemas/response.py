from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    """Base schema for API responses"""

    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None
