from flask import make_response, Response

from src.errors.default_error import DefaultError


async def response_error(error: DefaultError) -> Response:
    response = make_response({
        "error": error.message
    }, error.code)

    response.headers["Content-Type"] = "application/json"

    return response
