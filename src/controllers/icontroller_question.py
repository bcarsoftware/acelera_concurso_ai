from abc import ABC, abstractmethod

from flask import Request, Response


class IControllerQuestion(ABC):
    @abstractmethod
    async def generate_questions(self, request: Request) -> Response:
        pass

    @abstractmethod
    async def generate_question_from_pdf(self, request: Request) -> Response:
        pass
