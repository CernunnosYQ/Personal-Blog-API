from pydantic import ConfigDict

from app.schemas.user import UserBase


class UserExtended(UserBase):
    """
    Extended User model for testing purposes.
    """

    unhashed_password: str
    access_token: str

    model_config = ConfigDict(from_attributes=True)
