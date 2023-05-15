from app.models.mode_base import UpdateBase
from app.models.user.user import UserRoleEnum


class UserUpdate(UpdateBase):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    username: str | None = None
    is_active: bool | None = None
    role: UserRoleEnum | None = None
