import hashlib
import uuid
from typing import Tuple

from pydantic import root_validator

from app.models import User


class UserRaw(User):
    password_hash: str | None = None
    password_salt: str | None = None
    password: str | None

    @root_validator(pre=True)
    def update_password(cls, data_values: dict):
        data_values = dict(data_values)
        if "password" in data_values and data_values["password"] is not None:
            new_hash, new_salt = get_pass_hash(data_values["password"])
            data_values["password_hash"] = new_hash
            data_values["password_salt"] = new_salt
        return data_values

    def set_new_password(self, password: str):
        new_hash, new_salt = get_pass_hash(password)
        self.password_hash = new_hash
        self.password_salt = new_salt

    def validate_password(self, password: str) -> bool:
        saved_hash, _ = get_pass_hash(password, self.password_salt)
        return saved_hash == self.password_hash


def get_pass_hash(password: str, salt: str = None) -> Tuple[str, str]:
    if not salt:
        salt = get_random_string()

    enc = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,  # noqa: WPS432
    )
    return enc.hex(), salt


def get_random_string() -> str:
    return uuid.uuid4().hex
