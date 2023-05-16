from typing import TypeVar, Generic

from sqlalchemy import String, cast, or_, update, select, delete, func

from app.database.entity_base import OrmModel
from app.models.mode_base import ModelBase, UpdateBase

Entity = TypeVar("Entity", bound=OrmModel)
Model = TypeVar("Model", bound=ModelBase)


class BaseRepository(Generic[Model]):
    model: Model
    entity: Entity

    def __init__(self, db_session):
        self.db_session = db_session

    async def create(self, model: ModelBase) -> Model:
        async with self.db_session() as session:
            print('therererer')
            entity = self.entity.from_model(model)
            print(f'LOL KEK {entity = }')
            session.add(entity)
            await session.commit()

            await session.refresh(entity)
            return entity.to_model()

    async def bulk_create(self, models: list[Model]) -> None:
        async with self.db_session() as session:
            entities = tuple(map(self.entity.from_model, models))
            session.add_all(entities)
            await session.commit()

    async def bulk_update(self, models: list[Model], entity_instance=None) -> None:
        async with self.db_session() as session:
            for model in models:
                await self.save_entity_in_transaction(
                    session=session, model=model, entity_instance=entity_instance
                )
            await session.commit()

    async def save_entity(self, model: Model, entity_instance):
        async with self.db_session() as session:
            await self.save_entity_in_transaction(
                session=session,
                model=model,
                entity_instance=entity_instance,
            )
            await session.commit()

    async def save_entity_in_transaction(
            self, session, model: Model, entity_instance=None
    ):
        entity_instance = entity_instance if entity_instance else self.entity
        await session.execute(
            update(entity_instance)
            .where(entity_instance.id == model.id)
            .values(entity_instance.values_from_model(model))
        )

    async def save(self, model: Model, entity=None):
        await self.save_entity(model, entity if entity else self.entity)

    async def update(self, model: UpdateBase, entity: Entity = None) -> Model:
        await self.save(model, entity)
        return await self.get_by_id(model.id)

    async def delete_by_id(self, model_id: int):
        async with self.db_session() as session:
            await session.execute(delete(self.entity).where(self.entity.id == model_id))
            await session.commit()

    async def get_entity_by_id(
        self, model_id: int, entity_instance, model_instance=None
    ):
        async with self.db_session() as session:
            query = (
                select(entity_instance).limit(1).where(entity_instance.id == model_id)
            )
            entity = await session.scalar(query)

            return self.model_or_none(entity, model_instance)

    async def get_all(
        self,
        entity: Entity = None,  # type: ignore
    ) -> list[Model]:
        async with self.db_session() as session:
            query = select(entity if entity else self.entity)
            result = await session.execute(query)
            return self.get_list(result.scalars())

    async def get_by_id(self, model_id: int) -> Model | None:
        async with self.db_session() as session:
            query = select(self.entity).limit(1).where(self.entity.id == model_id)
            entity = await session.scalar(query)
            return self.model_or_none(entity)

    def get_list(self, query, model=None) -> list:
        model_to = model if model else self.model

        return [model_to.from_orm(entity) for entity in query]

    async def save_or_create_entity(self, session, entity_type, entity):
        if entity.id:
            await session.execute(
                update(entity_type)
                .where(entity_type.id == entity.id)
                .values(entity.to_values()),
            )
        else:
            session.add(entity)

    def model_or_none(self, entity, model=None):
        if not model:
            return entity.to_model() if entity else None
        return model.from_orm(entity) if entity else None

    def add_pagination(self, models: list, page: int, page_size: int) -> list:
        """Util function to make pagination from list"""
        left_idx = (page - 1) * page_size
        right_idx = left_idx + page_size
        return models[left_idx:right_idx]

    def add_sorting(self, query, sorting: tuple):
        if sorting:
            query = query.order_by(*sorting)
        return query

    async def get_total(self, session) -> int:
        count = await session.execute(
            select(func.count()).select_from(select(self.entity).subquery())
        )
        return count.scalar_one()

    def _add_search_by_fields(
        self,
        query,
        string_to_search: str,
        fields: list,
    ):
        string_to_search = string_to_search.rstrip()
        likes = []
        for field in fields:
            likes.append(
                cast(field, String).like(f"%{string_to_search}%"),
            )
        return query.filter(or_(*likes))
