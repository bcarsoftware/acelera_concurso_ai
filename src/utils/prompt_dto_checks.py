from re import match
from typing import Dict, Any

from src.core.constraints import HttpStatus
from src.core.regex import Regex
from src.errors.prompt_error import PromptError
from src.model.prompt_dto import PromptDTO
from src.utils.json_to_dto import json_to_dto


class PromptDTOChecks:
    @classmethod
    async def get_prompt_dto(cls, data: Dict[str, Any]) -> PromptDTO:
        prompt_error = PromptError(
            "data incompatible with the model prompt dto",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        result = await json_to_dto(data, prompt_error, PromptDTO)

        return PromptDTO.model_validate(result)

    @classmethod
    async def check_prompt_dto(cls, prompt_dto: PromptDTO) -> None:
        if not match(Regex.STRING_4_MIN, prompt_dto.value):
            raise PromptError("invalid prompt text", HttpStatus.BAD_REQUEST)

        if prompt_dto.params:
            for param in prompt_dto.params:
                if not match(Regex.STRING_2_MIN, param):
                    raise PromptError("invalid prompt param", HttpStatus.BAD_REQUEST)
