from src.core.constraints import HttpStatus
from src.errors.default_error import DefaultError


class PromptError(DefaultError):
    def __init__(self, message: str, code: int = HttpStatus.BAD_REQUEST) -> None:
        super().__init__(message, code)
