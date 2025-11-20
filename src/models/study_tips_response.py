from pydantic import BaseModel


class StudyTipsResponse(BaseModel):
    name: str
    description: str
    ai_generate: bool
