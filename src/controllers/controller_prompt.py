from flask import Request, Response

from src.core.constraints import HttpStatus
from src.controllers.icontroller_prompt import IControllerPrompt
from src.core.responses.response_success import response_success
from src.services.iservice_prompt import IServicePrompt
from src.services.service_prompt import ServicePrompt
from src.utils.prompt_dto_checks import PromptDTOChecks


class ControllerPrompt(IControllerPrompt):
    service_prompt: IServicePrompt

    def __init__(self) -> None:
        self.service_prompt = ServicePrompt()

    async def generate_questions(self, request: Request) -> Response:
        data_json = request.json

        prompt_dto = await PromptDTOChecks.get_prompt_dto(data_json)

        response = await self.service_prompt.generate_questions(prompt_dto)

        return await response_success(
            data=response,
            status_code=HttpStatus.OK
        )

    async def generate_study_tips(self, request: Request) -> Response:
        data_json = request.json

        prompt_dto = await PromptDTOChecks.get_prompt_dto(data_json)

        response = await self.service_prompt.generate_study_tips(prompt_dto)

        return await response_success(
            data=response.model_dump(),
            status_code=HttpStatus.OK
        )
