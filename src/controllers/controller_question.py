from flask import Request, Response

from src.controllers.icontroller_question import IControllerQuestion
from src.core.constraints import HttpStatus
from src.core.responses.response_success import response_success
from src.enums.enum_style import EnumStyle
from src.services.iservice_question import IServiceQuestion
from src.services.service_question import ServiceQuestion
from src.utils.law_page_content import law_page_content
from src.utils.question_checkers import QuestionChecks


class ControllerQuestion(IControllerQuestion):
    def __init__(self) -> None:
        self.service_question: IServiceQuestion = ServiceQuestion()

    async def generate_questions(self, request: Request) -> Response:
        payload = request.json

        question_dto = await QuestionChecks.convert_to_question_dto(payload)

        question_dto.format = (
            '{questions: [ {id: number, question: question-text, alternatives: [Certo, Errado], answer: correct answer}...]}'
            if question_dto.status == EnumStyle.RIGHT_WRONG else
            '{questions: [ {id: number, question: question-text, alternatives: [<letter> <string>...], answer: <letter> <string>}...]}'
        )

        if question_dto.law_link:
            question_dto.prompt += (
                ". Considering the content of the law sent as the base to generate the questions."
                + " Use that scope. Remove the articles or parts those were revoked or vetoed."
            )
            question_dto.subject = None
            question_dto.law_content = await law_page_content(question_dto.law_link)

        questions = await self.service_question.generate_questions(question_dto)

        return await response_success(
            data=questions.model_dump(mode="json"),
            status_code=HttpStatus.OK
        )
