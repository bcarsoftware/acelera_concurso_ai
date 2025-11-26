from typing import Dict, List

from flask import make_response, Response, send_file
from pydantic import BaseModel
from werkzeug.datastructures import FileStorage


async def response_success(data: Dict | List | BaseModel, status_code: int) -> Response:
    response = make_response(data, status_code)

    response.headers["Content-Type"] = "application/json"

    return response


async def response_success_file(data: FileStorage, status_code: int) -> Response:
    file = data.stream
    file.seek(0)

    response = make_response(send_file(
        file,
        mimetype=data.mimetype,
        as_attachment=True,
        download_name=data.filename,
    ))

    response.status_code = status_code
    return response
