import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase
from app.models import UserSession


class UserSessionEntity(Base, EntityBase[UserSession]):
    __tablename__ = "user_session"
    model = UserSession

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)
    user_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("user.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )
    token = sa.Column(sa.String, primary_key=True)
    refresh_token = sa.Column(sa.String)
    token_expired_at = sa.Column(sa.TIMESTAMP(True), nullable=False)

    refresh_token_expired_at = sa.Column(sa.TIMESTAMP(True))
