from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.models.base import Base

class QuestionBank(Base):
    __tablename__ = "t_question_bank"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_user.id"), index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    question_count: Mapped[int] = mapped_column(Integer, default=0)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否公开(预留)")
    price: Mapped[float] = mapped_column(Integer, default=0, comment="价格(预留)")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    
    questions: Mapped[list["Question"]] = relationship(back_populates="bank", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "t_question"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    bank_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_question_bank.id"), index=True)
    type: Mapped[str] = mapped_column(String(32), comment="single/multiple/true_false")
    stem: Mapped[str] = mapped_column(Text, comment="题干")
    options: Mapped[str] = mapped_column(Text, comment="选项JSON")
    answer: Mapped[str] = mapped_column(String(64), comment="正确答案")
    analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    md5: Mapped[str] = mapped_column(String(32), index=True, comment="去重哈希")
    
    bank: Mapped["QuestionBank"] = relationship(back_populates="questions")

class AnswerRecord(Base):
    __tablename__ = "t_answer_record"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="客户端生成的UUID")
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_user.id"), index=True)
    question_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_question.id"), index=True)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    answer: Mapped[str] = mapped_column(String(64))
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime, index=True)

class WrongQuestion(Base):
    __tablename__ = "t_wrong_question"
    
    user_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_user.id"), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(64), ForeignKey("t_question.id"), primary_key=True)
    wrong_count: Mapped[int] = mapped_column(Integer, default=1)
    last_wrong_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
