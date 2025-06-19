class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

    pass


class ConflictError(Exception):
    """Exception raised when there is a conflict, such as duplicate entries."""

    pass
