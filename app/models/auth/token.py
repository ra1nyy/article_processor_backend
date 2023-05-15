from datetime import datetime

from pydantic import BaseModel

from app.models.auth.user_session import UserSession
from app.models.user.enums import UserRoleEnum


class Token(BaseModel):
    access_token: str
    expires: datetime
    refresh_token: str
    token_type: str | None = "Bearer"
    user_role: UserRoleEnum

    @classmethod
    def from_session(cls, session: UserSession, user_role: UserRoleEnum) -> "Token":
        return Token(
            access_token=session.token,
            expires=session.token_expired_at,
            refresh_token=session.refresh_token,
            user_role=user_role,
        )
