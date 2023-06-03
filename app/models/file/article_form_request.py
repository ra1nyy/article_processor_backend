from app.models.file.article_form import FileBase
from app.models.mode_base import UpdateBase


class FileDomain(FileBase):
    id: int = None


class FileCreate(FileBase):
    ...


class FileUpdate(UpdateBase, FileBase):
    ...
