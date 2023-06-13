import os
import aiofiles
import uuid
from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.core.config import Config
from app.core.logger.appLogger import AppLogger
from app.models.article_form.article_form_request import ArticleFormDomain
from app.models.file.article_form_request import FileDomain
from app.services.base_service import BaseService
from app.services.doc_service.doc_service import DocService
from app.services.file.file_repository import FileRepository


class FileService(BaseService[FileDomain]):
    model = FileDomain
    repository: FileRepository

    def __init__(
        self,
        repository: FileRepository,
        doc_service: DocService,
        config: Config | None = None,
        logger: AppLogger | None = None,
    ) -> None:  # noqa
        super().__init__(repository, config=config, logger=logger)
        self.doc_service = doc_service

    @BaseService.catch_db_error(entity=ArticleFormDomain.__name__, unique_field="symbol")
    async def upload_document(self, file_doc: UploadFile) -> FileDomain:
        self.__prepare_paths()

        new_file_name = self.__generate_filename(file_doc.filename)

        async with aiofiles.open(
                os.path.join(self.config.attached_docs_path, new_file_name),
                'wb'
        ) as out_file:
            content = await file_doc.read()
            await out_file.write(content)

        uploaded_file = FileDomain(
            path=os.path.join(self.config.attached_docs_path, new_file_name),
            name=new_file_name,
            size_kb=int(file_doc.size / 1024),
        )

        return await self.repository.create(uploaded_file)

    async def load_document(self, file_id: int) -> FileResponse:
        file = await self.repository.get_entity_by_id(file_id)

        if not os.path.exists(file.path):
            raise FileNotFoundError(f'No such file :(\n{file.path}')

        return FileResponse(
            path=file.path,
            media_type='application/octet-stream',
            filename=file.name,
        )

    async def load_document_metadata(self, file_id: int) -> FileDomain:
        return await self.repository.get_entity_by_id(file_id)

    async def create_formatted_docx(
        self,
        article: ArticleFormDomain,
        attached_text: str | None,
        filename: str,
    ) -> FileDomain | None:
        self.__prepare_paths()

        if not attached_text:
            return None

        doc_file = self.doc_service.create_formatted_docx(
            article=article,
            attached_text=attached_text,
            filename=filename,
            filepath=self.config.formatted_docs_path,
        )

        return await self.create_entity(doc_file)

    def __prepare_paths(self):
        if not os.path.exists(self.config.formatted_docs_path):
            os.mkdir(self.config.formatted_docs_path)
        if not os.path.exists(self.config.attached_docs_path):
            os.mkdir(self.config.attached_docs_path)

    def __generate_filename(self, filename: str = 'unk') -> str:
        return f'{uuid.uuid4()}_{filename}'
