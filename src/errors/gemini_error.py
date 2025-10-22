from src.core.constraints import HttpStatus
from src.errors.default_error import DefaultError


class GeminiError(DefaultError):
    def __init__(self, message: str, code: int = HttpStatus.UNAUTHORIZED) -> None:
        super().__init__(message, code)
