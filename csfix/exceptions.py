from typing import Optional


class BaseError(Exception):
    def __init__(self, message: Optional[str] = None):
        if message:
            super().__init__(message)


class DatabaseNotConnectedError(BaseError):
    pass


class ToolNotFoundError(BaseError):
    pass
