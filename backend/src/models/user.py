from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.models.base import Base

class User(Base):
    __tablename__ = "t_user"
    
    # MySQL VARCHAR 需要指定长度
    id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="用户ID")
    openid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="微信OpenID")
    unionid: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True, comment="微信UnionID")
    nickname: Mapped[str | None] = mapped_column(String(64), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), comment="注册时间")
