from abc import ABC, abstractmethod

from flask import Response, Request


class IControllerPrompt(ABC):
    @abstractmethod
    async def generate_questions(self, request: Request) -> Response:
        pass
