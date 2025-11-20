from functools import wraps
from typing import Callable, Any

from flask import request

from src.core.constraints import HttpStatus, Token
from src.errors.jwt_error import JWTError


def authenticated(function: Callable[..., Any]):
    @wraps(function)
    async def wrapper(*args, **kwargs: Any) -> Any:
        headers = request.headers

        token = headers.get("Authorization")

        if token is None:
            raise JWTError("token authentication required", HttpStatus.UNAUTHORIZED)

        token = token.replace("Bearer", "").strip()

        try:
            if token != Token.PUBLIC_KEY:
                raise JWTError("token authentication invalid", HttpStatus.UNAUTHORIZED)

            if f"{token}{Token.SECRET_KEY}" != f"{Token.PUBLIC_KEY}{Token.SECRET_KEY}":
                raise JWTError("token authentication invalid", HttpStatus.UNAUTHORIZED)

            return await function(*args, **kwargs)
        except JWTError as jtw_e:
            print(jtw_e)
            raise JWTError(jtw_e.message, HttpStatus.UNAUTHORIZED)

    return wrapper
