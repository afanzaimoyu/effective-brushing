from datetime import datetime
from src.schemas.base import SchemaBase

class FavoriteResponse(SchemaBase):
    user_id: str
    question_id: str
    note: str | None
    created_at: datetime
