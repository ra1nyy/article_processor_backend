"""Contract for what we are giving to user in response."""
from app.models.mode_base import ModelBase


class UserResponse(ModelBase):
    """Simple contract with some excluded field that no need to responde."""

    #  id: int
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    username: str | None = None
    #  role: str = UserRoleEnum.USER
    #  created_at: datetime = datetime.utcnow()
    #  updated_at: datetime = datetime.utcnow()
    #  last_login: datetime = datetime.utcnow()
    is_active: bool | None = None
