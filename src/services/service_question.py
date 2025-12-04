import json
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, PageBreak, SimpleDocTemplate

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

        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]

        try:
            pdfmetrics.registerFont(TTFont("Inter", "font/Inter.ttf"))
            pdfmetrics.registerFontFamily("Inter", normal="Inter")
            style_normal.fontName = "Inter"
            style_normal.fontSize = 12
        except (FileNotFoundError, IOError):
            style_normal.fontName = "Helvetica"
        finally:
            style_normal.fontSize = 12

        pdf_file = BytesIO()

        page_settings = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch
        )

        flowable_list = []

        exam_content = (
            f"{question_response.public_tender.upper()}<br />" if question_response.public_tender else
            f"GERADOR DE QUESTÔES DE CONCURSOS<br />"
        )
        exam_content += (
            f"{question_response.board_name.upper()}<br />ACELERA CONCURSO<br />{"=" * 63}<br />"
            if question_response.board_name else f"ACELERA CONCURSO<br />{"=" * 63}<br />"
        )

        flowable_list.append(Paragraph(exam_content, style_normal))
        flowable_list.append(Spacer(1, 12))

        for content in contents:
            flowable_list.append(Paragraph(content, style_normal))
            flowable_list.append(Spacer(1, 8))

        flowable_list.append(PageBreak())

        for template in templates:
            flowable_list.append(Paragraph(template, style_normal))

        page_settings.build(flowable_list)

        return pdf_file.getvalue()
