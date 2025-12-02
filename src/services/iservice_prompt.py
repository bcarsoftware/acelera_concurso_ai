from abc import ABC, abstractmethod

from src.models.prompt_dto import PromptDTO
from src.models.prompt_response import PromptResponse
from src.models.study_tips_response import StudyTipsResponse


class IServicePrompt(ABC):
    @abstractmethod
    async def generate_questions(self, prompt_dto: PromptDTO) -> PromptResponse:
        pass

    @abstractmethod
    async def generate_study_tips(self, prompt_dto: PromptDTO) -> StudyTipsResponse:
        pass
