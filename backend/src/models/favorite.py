from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.models.base import Base

class Favorite(Base):
    __tablename__ = "t_favorite"
    
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_user.id"), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_question.id"), primary_key=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True, comment="收藏备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
