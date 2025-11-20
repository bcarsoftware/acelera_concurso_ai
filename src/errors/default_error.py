from abc import ABC

from src.core.constraints import HttpStatus


class DefaultError(ABC, RuntimeError):
    code: int
    message: str
    name: str

    def __init__(self, message: str, code: int = HttpStatus.BAD_REQUEST) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
