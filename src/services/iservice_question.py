from abc import ABC, abstractmethod

from src.models.question_dto import QuestionDTO
from src.models.question_response import QuestionResponse


class IServiceQuestion(ABC):
    @abstractmethod
    async def generate_questions(self, question_dto: QuestionDTO) -> QuestionResponse:
        pass
