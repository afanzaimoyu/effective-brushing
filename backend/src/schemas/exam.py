from pydantic import BaseModel
from datetime import datetime
from src.schemas.base import SchemaBase

class ExamCreateSchema(BaseModel):
    name: str = "模考"
    duration_minutes: int = 60
    question_count: int = 20
    source_bank_ids: list[str]

class ExamAnswerItem(BaseModel):
    question_id: str
    answer: str

class ExamSubmitSchema(BaseModel):
    answers: list[ExamAnswerItem]

class ExamResultResponse(BaseModel):
    exam_id: str
    total_score: int
    correct_count: int
    wrong_count: int
    wrong_list: list[str]
    
class ExamResponse(SchemaBase):
    id: str
    name: str
    duration_minutes: int
    total_score: int | None
    created_at: datetime
