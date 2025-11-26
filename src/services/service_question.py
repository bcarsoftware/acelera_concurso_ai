import json
from typing import Any

import pymupdf

from src.core.constraints import PagePaper
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

    async def generate_pdf_questions(self, question_response: QuestionResponse) -> bytes:
        content, template = await QuestionChecks.convert_question_response_to_string(question_response)

        text_area_rect = pymupdf.Rect(
            PagePaper.MARGIN,
            PagePaper.MARGIN,
            PagePaper.A4_WIDTH - PagePaper.MARGIN,
            PagePaper.A4_HEIGHT - PagePaper.MARGIN
        )

        with pymupdf.open() as pdf:
            page = pdf.new_page(width=PagePaper.A4_WIDTH, height=PagePaper.A4_HEIGHT)

            page.insert_textbox(
                text_area_rect,
                (f"{question_response.public_tender.upper()}\n" if question_response.public_tender else
                "GERADOR DE QUESTÔES DE CONCURSOS")+
                (f"{question_response.board_name.upper()}\nACELERA CONCURSO\n{"=" * 62}\n\n{content}" if question_response.board_name else
                "ACELERA CONCURSO"),
                fontsize=12,
                fontname="Inter",
                fontfile="font/Inter.ttf",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT
            )

            template_page = pdf.new_page(width=PagePaper.A4_WIDTH, height=PagePaper.A4_HEIGHT)

            template_page.insert_textbox(
                text_area_rect,
                template,
                fontsize=12,
                fontname="Inter",
                fontfile="font/Inter.ttf",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT
            )

            pdf_file = pdf.convert_to_pdf()

        return pdf_file
