from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.models.base import Base

class Exam(Base):
    __tablename__ = "t_exam"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_user.id"), index=True)
    name: Mapped[str] = mapped_column(String(128))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    total_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    questions_snapshot: Mapped[str | None] = mapped_column(Text, comment="试题ID列表快照(JSON)")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
