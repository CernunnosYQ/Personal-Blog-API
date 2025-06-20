from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    """Base schema for API responses"""

    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None
