from functools import wraps
from typing import Generic, TypeVar
from sqlalchemy import exc

from app.api.errors import (
    EntityCreateError,
    EntityNotFound,
    IncorrectServiceIntanse,
)
from app.core.config import Config
from app.core.logger.appLogger import AppLogger
from app.database.base_repository import BaseRepository
from app.models.mode_base import ModelBase, UpdateBase

Model = TypeVar("Model", bound=ModelBase)


class BaseService(Generic[Model]):
    model: Model
    """BaseService service for CRUD operations."""

    def __init__(
        self,
        repository: BaseRepository[Model],
        config: Config | None = None,
        logger: AppLogger | None = None,
    ) -> None:  # noqa
        self.config = config
        self.repository = repository
        self.logger = logger

    async def get_entity_by_id(self, entity_id: int) -> Model:
        """Base method for get Entity by its UID."""
        model = await self.repository.get_by_id(entity_id)

        if not model:
            self.logger.exception(msg=f'Entity{" "+self.model.__name__} not found')
            raise EntityNotFound(self.model.__name__)

        return model

    async def get_all_entities(
        self,
    ) -> list[Model | None]:
        """Base method for get all entities."""
        return await self.repository.get_all()

    async def create_entity(self, entity_to_create: ModelBase) -> Model:
        """Base method to create entity."""
        return await self.repository.create(entity_to_create)

    async def bulk_create_entities(self, entities_to_create: list[ModelBase]) -> None:
        """Base method to bulk create entities."""
        return await self.repository.bulk_create(entities_to_create)

    async def update_entity(self, update_entity_request: UpdateBase) -> Model:
        model = await self.repository.update(update_entity_request)

        if not model:
            self.logger.exception(f'Entity{" "+self.model.__name__} not found')
            raise EntityNotFound(self.model.__name__)

        return model

    async def _get_entities_for_update(self, models: list[UpdateBase]):
        """
        condition for filter - id exist
        """
        return [model for model in models if model.id is not None]

    async def _get_entities_for_create(self, models: list[UpdateBase]):
        """
        condition for filter - id not exist
        """
        return [model for model in models if model.id is None]

    @staticmethod
    def catch_db_error(
        entity,
        unique_field: str | None = None,
    ):
        """Decorator for catches error from DB."""

        def decorator(func):
            @wraps(func)
            async def wrapper(
                *args,
                **kwargs,
            ):
                if not getattr(args[0], "logger", False):
                    raise IncorrectServiceIntanse("No logger found in service instanse")
                try:
                    return await func(*args, **kwargs)
                except exc.IntegrityError as error:
                    if unique_field is None:
                        # Logging error
                        args[0].logger.exception(f"Cannot create {entity} because smth is wrong with " f"ForeignKey")

                        raise EntityCreateError(entity)

                    unique_field_value = args[1].dict(include={unique_field})[unique_field]
                    error_to_raise = EntityCreateError(
                        entity,
                        unique_field=unique_field,
                        unique_entity_field_name=unique_field_value,
                    )
                    # Logging error
                    args[0].logger.exception(
                        f"{entity} with {unique_field} '{unique_field_value}' already " 
                        f"exists",
                        extra={"error_short_description": error},
                    )

                    raise error_to_raise

            return wrapper

        return decorator
