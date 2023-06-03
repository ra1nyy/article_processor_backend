from app.database.base_repository import BaseRepository
from app.database.entities import FileEntity
from app.models.file.article_form_request import FileDomain


class FileRepository(BaseRepository[FileDomain]):
    model = FileDomain
    entity = FileEntity
