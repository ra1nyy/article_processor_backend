import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase


class AntiPlagiarismResultEntity(Base, EntityBase[...]):
    __tablename__ = "anti_plagiarism_result"
    model = ...

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)

    article_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("article_form.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
    )
    percentage_of_uniqueness = sa.Column(sa.INTEGER, nullable=False)

    updated_at = sa.Column(
        sa.TIMESTAMP(True),
        nullable=False,
        server_default=sa.func.now(),
        server_onupdate=sa.func.now(),
    )