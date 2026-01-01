from pydantic import BaseModel, field_validator
from datetime import datetime
from src.schemas.base import SchemaBase
import json

# --- Question Schemas ---
class QuestionBase(BaseModel):
    type: str
    stem: str
    options: list[str]
    answer: str
    analysis: str | None = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    type: str | None = None
    stem: str | None = None
    options: list[str] | None = None
    answer: str | None = None
    analysis: str | None = None

class QuestionResponse(QuestionBase, SchemaBase):
    id: str
    bank_id: str
    md5: str

    @field_validator('options', mode='before')
    @classmethod
    def parse_options(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        return v

# --- Sync Schemas ---
class AnswerRecordSchema(BaseModel):
    local_id: str
    bank_id: str | None = None
    question_id: str
    answer: str
    is_correct: bool
    duration_ms: int = 0
    answered_at: datetime
    
class SyncRequest(BaseModel):
    records: list[AnswerRecordSchema]

class SyncResponse(BaseModel):
    success_ids: list[str]
    failed_ids: list[str]
    server_timestamp: float
