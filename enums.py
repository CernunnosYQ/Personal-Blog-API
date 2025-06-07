from enum import Enum


class UserRoles(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

    def __str__(self):
        return self.name

    def is_admin(self):
        return self in (UserRoles.OWNER, UserRoles.ADMIN)
