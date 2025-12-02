import json

from src.core.constraints import HttpStatus
from src.errors.prompt_error import PromptError
from src.gemini.gemini import Gemini
from src.models.prompt_dto import PromptDTO
from src.models.prompt_response import PromptResponse
from src.models.study_tips_response import StudyTipsResponse
from src.services.iservice_prompt import IServicePrompt
from src.utils.prompt_dto_checks import PromptDTOChecks


class ServicePrompt(IServicePrompt):
    async def generate_questions(self, prompt_dto: PromptDTO) -> PromptResponse:
        await PromptDTOChecks.check_prompt_dto(prompt_dto)

        return await Gemini.generate_content(prompt_dto)

    async def generate_study_tips(self, prompt_dto: PromptDTO) -> StudyTipsResponse:
        prompt_dto.params = []
        prompt_dto.params.append("""
        Return the text following the format:
        {
            "name": <string>,
            "description": <string>,
        }
        Similar to a python dictionary.
        """)
        prompt_dto.params.append("Don't comment anything, just give me the request format.")
        prompt_dto.params.append("""
        name max length is: 128
        description max length is: 256
        """)
        prompt_dto.params.append("Don't use bold or italic.")
        prompt_dto.params.append("Be consistent.")
        prompt_dto.params.append("Be motivational oriented.")

        await PromptDTOChecks.check_prompt_dto(prompt_dto)

        text = await Gemini.generate_content(prompt_dto)

        text.text = text.text.replace("```json", "").replace("```", "")

        object_json = json.loads(text.text)

        if object_json.keys() != {"name", "description"}:
            raise PromptError(
                message="object don't corresponds the required data",
                code=HttpStatus.BAD_REQUEST
            )

        return StudyTipsResponse(
            name=f"[AI] {object_json['name']}",
            description=object_json["description"],
            ai_generate=True
        )
