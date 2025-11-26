from typing import Dict, Any, Tuple

from src.core.constraints import HttpStatus
from src.errors.question_error import QuestionError
from src.models.question_dto import QuestionDTO
from src.models.question_response import QuestionResponse
from src.utils.payload_dto import payload_dto


class QuestionChecks:
    @classmethod
    async def convert_to_question_dto(cls, payload: Dict[str, Any]) -> QuestionDTO:
        error = QuestionError(
            "payload doesn't match required data",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        question_dto = await payload_dto(payload, QuestionDTO, error)

        return QuestionDTO(**question_dto.model_dump())

    @classmethod
    async def convert_to_question_response(cls, payload: Dict[str, Any]) -> QuestionResponse:
        error = QuestionError(
            "payload doesn't match required data",
            HttpStatus.UNPROCESSABLE_ENTITY
        )

        question_response = await payload_dto(payload, QuestionResponse, error)

        return QuestionResponse(**question_response.model_dump())

    @classmethod
    async def convert_question_response_to_string(cls, question_response: QuestionResponse) -> Tuple[str, str]:
        if not question_response.questions:
            raise QuestionError("questions can't be empty", HttpStatus.BAD_REQUEST)

        content = ""
        template = f"GABARITO DE RESPOSTAS\nACELERA CONCURSO\n{"=" * 62}"

        for question in question_response.questions:
            content += f"{question.id}. {question.question}\n\n"
            letter = 65
            for alternative in question.alternatives:
                content += f"{chr(letter)}) {alternative}\n"
                letter += 1
            content += "\n"
            index_answer = question.alternatives.index(question.answer)
            letter = 65 + index_answer
            template += f"{question.id}. {chr(letter)})\n"

        return content, template

    @classmethod
    async def make_validation(cls, question_dto: QuestionDTO) -> None:
        if not question_dto.prompt:
            raise QuestionError("prompt can't be empty", HttpStatus.BAD_REQUEST)
        if question_dto.questions < 1:
            raise QuestionError("questions can't be less than 1", HttpStatus.BAD_REQUEST)
        if question_dto.public_tender and len(question_dto.public_tender) < 1:
            raise QuestionError("public tender can't be empty if set", HttpStatus.BAD_REQUEST)
        if question_dto.subject and len(question_dto.subject) < 1:
            raise QuestionError("subject can't be empty if set", HttpStatus.BAD_REQUEST)
        if question_dto.board_name and len(question_dto.board_name) < 1:
            raise QuestionError("board name can't be empty if set", HttpStatus.BAD_REQUEST)
        if question_dto.topic and len(question_dto.topic) < 1:
            raise QuestionError("topic can't be empty if set", HttpStatus.BAD_REQUEST)
        if question_dto.law_link and len(question_dto.law_link) < 1:
            raise QuestionError("law link can't be empty if set", HttpStatus.BAD_REQUEST)
        if question_dto.law_link and "https://" not in question_dto.law_link:
            raise QuestionError("invalid law link if set", HttpStatus.BAD_REQUEST)
