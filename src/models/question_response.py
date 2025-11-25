from typing import List, Optional

from pydantic import BaseModel


class Question(BaseModel):
    id: int
    question: str
    alternatives: List[str]
    answer: str


class QuestionResponse(BaseModel):
    questions: List[Question] = []
