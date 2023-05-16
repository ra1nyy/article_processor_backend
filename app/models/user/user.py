from datetime import datetime

from app.models.mode_base import ModelBase
from app.models.user.enums import UserRoleEnum


class User(ModelBase):
    id: int
    first_name: str
    last_name: str
    surname: str
    username: str
    email: str

    place_of_study: str
    study_group_number: str

    place_of_work: str | None = None
    social_network_url: str | None = None

    role: UserRoleEnum = UserRoleEnum.USER
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    last_login: datetime = datetime.utcnow()
    is_active: bool
