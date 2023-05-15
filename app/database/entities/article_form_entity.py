import sqlalchemy as sa

from app.database.base import Base
from app.database.entity_base import EntityBase


class ArticleFormEntity(Base, EntityBase[...]):
    __tablename__ = "article_form"
    model = ...

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)

    name = sa.Column(sa.VARCHAR, nullable=True)
    annotation = sa.Column(sa.VARCHAR, nullable=True)

    scientific_adviser_fullname = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_academic_degree = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_academic_title = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_institute = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_department = sa.Column(sa.VARCHAR, nullable=True)

    formatted_docs_filename = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("file.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=True,
    )
    attached_docs_filename = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("file.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=True,
    )

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
