from typing import Dict, List

from flask import make_response, Response
from pydantic import BaseModel


async def response_success(data: Dict | List | BaseModel, status_code: int) -> Response:
    response = make_response(data, status_code)

    response.headers["Content-Type"] = "application/json"

    return response
