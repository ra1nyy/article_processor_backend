from datetime import datetime

from pydantic import Field, validator

from app.api.errors import WrongDataError
from app.models import User
from app.models.mode_base import ModelBase


class ArticleFormBase(ModelBase):
    """Base model for Num."""

    name: str = None
    annotation: str = None

    scientific_adviser_fullname: str = None
    scientific_adviser_academic_degree: str = None
    scientific_adviser_academic_title: str = None
    scientific_adviser_institute: str = None
    scientific_adviser_department: str = None

    # formatted_docs_filename: str | None = None
    # attached_docs_filename: str | None = None
    # attached_article_text: str | None = None

    created_at: datetime | None = Field(
        default=datetime.utcnow(),
        description="Дата создания операции",
    )
    updated_at: datetime = None

    # @validator('attached_docs_filename')
    # def validate_attached_docs(cls, value, values: dict):
    #     print(values)
    #     print(value)
    #     if values.get('attached_docs_filename') and values.get('attached_article_text'):
    #         raise WrongDataError(message='Should be only file or text, not together')
    #     return value
