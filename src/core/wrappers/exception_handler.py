from functools import wraps
from typing import Callable

from src.core.responses.response_error import response_error
from src.errors.default_error import DefaultError


def exception_handler(function: Callable) -> Callable:
    @wraps
    async def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except DefaultError as error:
            return await response_error(error)
    return wrapper
