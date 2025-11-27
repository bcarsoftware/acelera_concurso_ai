import json
from typing import Any

import pymupdf

from src.core.constraints import PagePaper
from src.errors.question_error import QuestionError
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
        contents, templates = await QuestionChecks.convert_question_response_to_string(question_response)

        if len(contents) < 1 or len(templates) < 1:
            raise QuestionError("empty data can't be used")

        text_area_rect = pymupdf.Rect(
            PagePaper.MARGIN,
            PagePaper.MARGIN,
            PagePaper.A4_WIDTH - PagePaper.MARGIN,
            PagePaper.A4_HEIGHT - PagePaper.MARGIN
        )

        exam_content = (
            f"{question_response.public_tender.upper()}\n" if question_response.public_tender else
            f"GERADOR DE QUESTÔES DE CONCURSOS\n"
        )
        exam_content += (
            f"{question_response.board_name.upper()}\nACELERA CONCURSO\n{"=" * 62}\n"
            if question_response.board_name else f"ACELERA CONCURSO\n{"=" * 62}\n"
        )

        with pymupdf.open() as pdf:
            for content in contents:
                page = pdf.new_page(width=PagePaper.A4_WIDTH, height=PagePaper.A4_HEIGHT)

                page.insert_textbox(
                    text_area_rect,
                    exam_content + content,
                    fontsize=12,
                    fontname="Inter",
                    fontfile="font/Inter.ttf",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_LEFT
                )
                exam_content = ""

            for template in templates:
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
