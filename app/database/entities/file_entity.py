import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase
from app.models.file.article_form_request import FileDomain


class FileEntity(Base, EntityBase[FileDomain]):
    __tablename__ = "file"
    model = FileDomain

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
