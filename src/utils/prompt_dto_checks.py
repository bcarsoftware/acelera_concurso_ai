from re import match

from src.core.constraints import HttpStatus
from src.core.regex import Regex
from src.errors.prompt_error import PromptError
from src.model.prompt_dto import PromptDTO


class PromptDTOChecks:
    @classmethod
    async def check_prompt_dto(cls, prompt_dto: PromptDTO) -> None:
        if not match(Regex.STRING_4_MIN, prompt_dto.value):
            raise PromptError("invalid prompt text", HttpStatus.BAD_REQUEST)

        if prompt_dto.params:
            for param in prompt_dto.params:
                if not match(Regex.STRING_2_MIN, param):
                    raise PromptError("invalid prompt param", HttpStatus.BAD_REQUEST)
