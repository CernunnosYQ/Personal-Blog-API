from enum import Enum


class UserRoles(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

    def __str__(self) -> str:
        return self.name

    def is_admin(self) -> bool:
        return self in (UserRoles.OWNER, UserRoles.ADMIN)


class Tier(Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def allowed_tiers(cls) -> set[str]:
        return {tier.value for tier in cls}
