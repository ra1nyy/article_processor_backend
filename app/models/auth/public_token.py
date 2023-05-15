from datetime import datetime

from pydantic.main import BaseModel


class PublicToken(BaseModel):
    id: int = None
    user_id: str
    token: str
    expired_at: datetime
    done: bool = False
