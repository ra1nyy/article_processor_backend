import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase


class FileEntity(Base, EntityBase[...]):
    __tablename__ = "file"
    model = ...

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)

    path = sa.Column(sa.VARCHAR, nullable=True)
    name = sa.Column(sa.VARCHAR, nullable=True)
    size_kb = sa.Column(
        sa.INTEGER,
        nullable=False,
    )

    created_at = sa.Column(
        sa.TIMESTAMP(True),
        nullable=False,
        server_default=sa.func.now(),
    )
