from typing import Any, Type

from pydantic import BaseModel, ValidationError

from src.errors.default_error import DefaultError
from src.utils.strip_strings import strip_strings


async def payload_dto(payload: Any, type_dto: Type[BaseModel], exception_obj: DefaultError):
    data = await strip_strings(payload)

    try:
        return type_dto.model_validate(data)
    except ValidationError as ve:
        print(ve.errors)
        raise exception_obj
