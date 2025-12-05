from typing import Optional

from pydantic import BaseModel

from src.enums.enum_language import EnumLanguage
from src.enums.enum_level import EnumLevel
from src.enums.enum_style import EnumStyle


class QuestionDTO(BaseModel):
    level: EnumLevel
    status: EnumStyle

    prompt: str
    questions: int
    format: Optional[str] = None

    language: Optional[EnumLanguage] = EnumLanguage.BRAZILIAN

    public_tender: Optional[str] = None
    subject: Optional[str] = None
    board_name: Optional[str] = None
    topic: Optional[str] = None
    law_link: Optional[str] = None
    law_content: Optional[str] = None
    pdf_content: Optional[str] = None

    @property
    def string(self) -> str:
        value = f"{
            self.prompt + ". Without alternatives like: A). Only the alternative text." +
            " The answer MUST BE the same text found at the alternative list, without any explanation."
        }\nquestions: {self.questions}. Don't use any introductory information or posterior, only the required format."
        value += f"language: {self.language.value}\n"
        value += f"level: {self.level.value}\nstatus: {self.status.value}\n"
        value += f"unique and exclusive return format (it must be involved in markdown text like: ```json...```): {self.format}\n"

        value += f"public tender exam: {self.public_tender}\n" if self.public_tender else ""
        value += f"subject: {self.subject}\n" if self.subject else ""
        value += f"board name: {self.board_name}\n" if self.board_name else ""
        value += f"topic: {self.topic}\n" if self.topic else ""
        value += f"law content: {self.law_content}\n" if self.law_content else ""
        value += f"pdf_content: {self.pdf_content}" if self.pdf_content else ""

        value = value.strip().lower()

        return value
