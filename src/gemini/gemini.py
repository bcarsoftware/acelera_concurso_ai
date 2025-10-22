import asyncio

from google import genai
from google.genai.errors import ClientError

from src.core.constraints import Environ, GeminiModel, HttpStatus
from src.errors.gemini_error import GeminiError
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

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt_dto.string
            )

            return PromptResponse(text=response.text)
        except ClientError as c_e:
            print(str(c_e))
            raise GeminiError(c_e.message.lower(), HttpStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(str(e))
            raise GeminiError("Internal server error", HttpStatus.INTERNAL_SERVER_ERROR)
