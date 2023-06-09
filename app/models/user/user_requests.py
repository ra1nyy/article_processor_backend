from pydantic import EmailStr, SecretStr
from app.models.mode_base import UpdateBase, ModelBase


class UserUpdate(UpdateBase):
    first_name: str | None = None
    last_name: str | None = None
    surname: str | None = None

    username: str | None = None
    email: str | None = None

    place_of_study: str | None = None
    study_group_number: str | None = None

    place_of_work: str | None = None
    social_network_url: str | None = None


class UserRegisterRequest(ModelBase):
    email: EmailStr
    password: str

    first_name: str
    last_name: str
    surname: str
    username: str

    place_of_study: str
    study_group_number: str
