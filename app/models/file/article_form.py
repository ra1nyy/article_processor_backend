from datetime import datetime
from pydantic import Field

from app.models.mode_base import ModelBase


class FileBase(ModelBase):
    """Base model for Num."""

    path: str = None
    name: str = None

    size_kb: int = None
    created_at: datetime | None = Field(
        default=datetime.utcnow(),
        description="Дата загрузки файла",
    )
