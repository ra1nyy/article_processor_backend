from typing import Generic, Type, TypeVar

from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from app.models.mode_base import ModelBase

OrmModel = declarative_base()

Entity = TypeVar("Entity", bound=OrmModel)
Model = TypeVar("Model", bound=ModelBase)


class EntityBase(Generic[Model]):
    model: Type[Model] = None
    update_ignore_fields = {"id", "updated_at"}

    def __init__(self, *args, **kwargs):
        pass  # noqa: WPS420

    @classmethod
    def from_model(cls: Type[Entity], model: Model) -> Entity:
        # TODO:
        data_values = {}
        colls = inspect(cls).mapper.column_attrs
        for coll in colls:
            col_name = coll.key
            try:
                data_values[col_name] = getattr(model, col_name)
            except AttributeError:
                pass  # noqa: WPS420
        return cls(**data_values)

        # return cls(**model.dict())

    @classmethod
    def values_from_model(cls: Type[Entity], model: Model) -> dict:
        data_values = {}
        colls = inspect(cls).mapper.column_attrs
        update_ignore_fields = cls.update_ignore_fields
        for coll in colls:
            value = getattr(model, coll.key, None)
            if value and coll.key not in update_ignore_fields:
                data_values[coll.key] = value
        return data_values

    def to_values(self) -> dict:
        data_values = {}
        colls = inspect(self).mapper.column_attrs
        for coll in colls:
            col_name = coll.key
            if col_name in self.update_ignore_fields:
                continue
            data_values[col_name] = getattr(self, col_name)
        return data_values

    def to_model(self) -> Model:
        return self.model.from_orm(self)
