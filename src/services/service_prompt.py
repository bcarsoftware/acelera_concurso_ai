from src.gemini.gemini import Gemini
from src.models.prompt_dto import PromptDTO
from src.models.prompt_resp import PromptResponse
from src.services.iservice_prompt import IServicePrompt
from src.utils.prompt_dto_checks import PromptDTOChecks


class ServicePrompt(IServicePrompt):
    async def generate_questions(self, prompt_dto: PromptDTO) -> PromptResponse:
        await PromptDTOChecks.check_prompt_dto(prompt_dto)

        return await Gemini.generate_content(prompt_dto)
