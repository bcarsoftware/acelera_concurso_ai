from abc import ABC, abstractmethod

from src.model.prompt_dto import PromptDTO
from src.model.prompt_resp import PromptResponse


class IServicePrompt(ABC):
    @abstractmethod
    async def generate_questions(self, prompt_dto: PromptDTO) -> PromptResponse:
        pass
