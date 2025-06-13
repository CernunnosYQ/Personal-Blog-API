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


class Tier(Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    def __str__(self):
        return self.name

    @classmethod
    def allowed_tiers(cls):
        return {tier.value for tier in cls}
