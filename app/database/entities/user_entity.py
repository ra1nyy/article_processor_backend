import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase
from app.models import User, UserRaw


class UserEntity(Base, EntityBase[User]):
    __tablename__ = "user"
    model = UserRaw

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)
    username = sa.Column(sa.String(30), nullable=False, unique=True)
    email = sa.Column(sa.String(100), nullable=False, unique=True)
    role = sa.Column(sa.String(20), nullable=False)

    first_name = sa.Column(sa.VARCHAR, nullable=False)
    last_name = sa.Column(sa.VARCHAR, nullable=False)
    surname = sa.Column(sa.VARCHAR, nullable=False)

    place_of_study = sa.Column(sa.VARCHAR, nullable=False)
    study_group_number = sa.Column(sa.VARCHAR, nullable=False)
    place_of_work = sa.Column(sa.VARCHAR, nullable=True)

    social_network_url = sa.Column(sa.VARCHAR, nullable=True)

    password_hash = sa.Column(sa.VARCHAR, nullable=False)
    password_salt = sa.Column(sa.VARCHAR, nullable=False)

    is_active = sa.Column(sa.BOOLEAN, nullable=False, default=False)

    created_at = sa.Column(
        sa.TIMESTAMP(True),
        server_default=sa.func.now(),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.TIMESTAMP(True),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
    last_login = sa.Column(
        sa.TIMESTAMP(True),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )
