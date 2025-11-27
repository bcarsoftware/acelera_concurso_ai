from io import BytesIO

from flask import Request, Response
from werkzeug.datastructures import FileStorage

from src.controllers.icontroller_question import IControllerQuestion
from src.core.constraints import HttpStatus
from src.core.responses.response_success import response_success, response_success_file
from src.enums.enum_style import EnumStyle
from src.errors.question_error import QuestionError
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

        question_dto.format = await self._get_format_(question_dto.status)

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

    async def generate_question_from_pdf(self, request: Request) -> Response:
        pdf_file = request.files.get("pdf_file")
        form = dict(request.form)

        if not pdf_file:
            raise QuestionError("pdf file not provided", HttpStatus.BAD_REQUEST)

        question_dto = await QuestionChecks.convert_to_question_dto(form)

        question_dto.prompt += (
            ". Consider the content of param sent here named 'pdf_content' as the base to generate the questions."
        )

        question_dto.format = await self._get_format_(question_dto.status)

        response = await self.service_question.generate_question_from_pdf(pdf_file.stream.read(), question_dto)

        return await response_success(
            data=response.model_dump(mode="json"),
            status_code=HttpStatus.OK
        )

    async def generate_pdf_questions(self, request: Request) -> Response:
        payload = request.json

        question_response = await QuestionChecks.convert_to_question_response(payload)

        data = await self.service_question.generate_pdf_questions(question_response)
        pdf_file = FileStorage(
            stream=BytesIO(data),
            filename="concurso-publico-e-gabarito.pdf",
            content_type="application/pdf"
        )

        return await response_success_file(
            data=pdf_file,
            status_code=HttpStatus.OK
        )

    @staticmethod
    async def _get_format_(status: EnumStyle) -> str:
        return (
            '{questions: [ {id: number, question: question-text, alternatives: [Certo, Errado], answer: correct answer}...]}'
            if status == EnumStyle.RIGHT_WRONG else
            '{questions: [ {id: number, question: question-text, alternatives: [<string>...], answer: <string>}...]}'
        )
