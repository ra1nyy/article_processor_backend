import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.database.base import Base
from app.database.entities.user_entity import UserEntity
from app.database.entity_base import EntityBase
from app.models.article_form.article_form_request import ArticleFormDomain


class ArticleFormEntity(Base, EntityBase[ArticleFormDomain]):
    __tablename__ = "article_form"
    model = ArticleFormDomain

    id = sa.Column(sa.INTEGER, sa.Identity(), primary_key=True, nullable=False)

    name = sa.Column(sa.VARCHAR, nullable=True)
    annotation = sa.Column(sa.VARCHAR, nullable=True)

    scientific_adviser_fullname = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_academic_degree = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_academic_title = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_institute = sa.Column(sa.VARCHAR, nullable=True)
    scientific_adviser_department = sa.Column(sa.VARCHAR, nullable=True)

    formatted_docs_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("file.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=True,
    )
    attached_docs_id = sa.Column(
        sa.INTEGER,
        sa.ForeignKey("file.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=True,
    )
    list_of_references = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )

    keywords_rus = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )
    keywords_eng = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )

    title_rus = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )
    title_eng = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )

    abstract_rus = sa.Column(
        sa.VARCHAR,
        nullable=True,
    )
    abstract_eng = sa.Column(
        sa.VARCHAR,
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

    authors: Mapped[list[UserEntity]] = relationship(
        "UserEntity",
        secondary="article_author",
        lazy="joined",
    )

