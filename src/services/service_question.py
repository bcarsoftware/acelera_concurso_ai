import json

from src.gemini.gemini import Gemini
from src.models.question_dto import QuestionDTO
from src.models.question_response import QuestionResponse
from src.services.iservice_question import IServiceQuestion
from src.utils.pdf_util import PDFUtil
from src.utils.question_checkers import QuestionChecks


class ServiceQuestion(IServiceQuestion):
    async def generate_questions(self, question_dto: QuestionDTO) -> QuestionResponse:
        await QuestionChecks.make_validation(question_dto)

        data = await Gemini.generate_questions(question_dto)

        data.text = data.text.replace("```json", "").replace("```", "").strip()

        object_json = json.loads(data.text)

        return QuestionResponse.model_validate(object_json)

    async def generate_question_from_pdf(self, pdf_file: bytes, question_dto: QuestionDTO) -> QuestionResponse:
        await QuestionChecks.make_validation(question_dto)

        pdf_data = await PDFUtil.get_pdf_text_content(pdf_file)

        question_dto.pdf_content = pdf_data

        data = await Gemini.generate_questions(question_dto)

        data.text = data.text.replace("```json", "").replace("```", "").strip()

        object_json = json.loads(data.text)

        return QuestionResponse.model_validate(object_json)
