from google import genai

from src.core.constraints import Environ, GeminiModel
from src.model.prompt_dto import PromptDTO
from src.model.prompt_resp import PromptResponse


class Gemini:
    @staticmethod
    async def _client_() -> genai.Client:
        return genai.Client(api_key=Environ.GEMINI_API_KEY)

    @staticmethod
    async def _get_model_() -> str:
        return {
            "Flash": GeminiModel.FLASH,
            "Pro": GeminiModel.PRO,
            "FlashLight": GeminiModel.FLASH_LIGHT,
        }.get(Environ.SELECT_MODEL, "")

    @classmethod
    async def generate_content(cls, prompt_dto: PromptDTO) -> PromptResponse:
        client = await cls._client_()

        model = await cls._get_model_()

        response = client.models.generate_content(
            model=model,
            contents=prompt_dto.string
        )

        return PromptResponse(text=response.text)
