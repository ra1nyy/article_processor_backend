from datetime import datetime

from app.models.mode_base import ModelBase


class UserSession(ModelBase):
    id: int = None
    user_id: int
    token: str
    refresh_token: str
    token_expired_at: datetime
    refresh_token_expired_at: datetime | None = None

    class Config:
        orm_mode = True
