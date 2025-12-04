import json
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, PageBreak, Frame, PageTemplate, BaseDocTemplate

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

        page_width, page_height = A4
        margin = 0.5 * inch
        column_gap = 0.25 * inch

        column_width = (page_width - 2 * margin - column_gap) / 2
        column_height = page_height - 2 * margin

        first_column = Frame(
            x1=margin,
            y1=margin,
            width=column_width,
            height=column_height,
            leftPadding=6,
            bottomPadding=6,
            rightPadding=6,
            topPadding=6
        )

        second_column = Frame(
            x1=margin + column_width + column_gap,
            y1=margin,
            width=column_width,
            height=column_height,
            leftPadding=6,
            bottomPadding=6,
            rightPadding=6,
            topPadding=6
        )

        multi_columns = PageTemplate(id="two_columns", frames=[first_column, second_column])

        page_settings = BaseDocTemplate(
            pdf_file,
            pagesize=A4,
            title="Questionário de Concurso Público",
            author="ACELERA CONCURSO",
            creator="ACELERA CONCURSO | Gerador de PDF"
        )

        page_settings.addPageTemplates([multi_columns])

        flowable_list = []

        exam_content = (
            f"{question_response.public_tender.upper()}<br />" if question_response.public_tender else
            f"GERADOR DE QUESTÔES DE CONCURSOS<br />"
        )
        exam_content += (
            f"{question_response.board_name.upper()}<br />ACELERA CONCURSO<br />{"=" * 30}<br />"
            if question_response.board_name else f"ACELERA CONCURSO<br />{"=" * 30}<br />"
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
