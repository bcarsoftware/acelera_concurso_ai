from typing import Dict, Any, Type

from pydantic import BaseModel, ValidationError

from src.errors.default_error import DefaultError


async def json_to_dto(
    data: Dict[str, Any],
    exception: DefaultError,
    dto_class: Type[BaseModel]
) -> BaseModel:
    try:
        return dto_class.model_validate(data)
    except ValidationError as e:
        print(str(e))
        raise exception
