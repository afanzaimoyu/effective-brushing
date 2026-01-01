from pydantic import BaseModel
from src.schemas.base import SchemaBase

class LoginRequest(BaseModel):
    code: str
    platform: str = "wechat_mini"

class TokenResponse(BaseModel):
    token: str
    expires_in: int
    is_new_user: bool

class UserInfo(SchemaBase):
    id: str  # id in DB, user_id in API response? Let's check API definition. API says "user_id". I should alias it or use response_model mapping.
    nickname: str | None
    avatar_url: str | None
