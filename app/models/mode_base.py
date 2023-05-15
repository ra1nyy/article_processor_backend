import copy

from pydantic import BaseModel

from app.api.errors import MissDataError


class ModelBase(BaseModel):
    def updated_copy(self, update_values: dict):
        updated_values = self.dict() | update_values
        return self.__class__(**updated_values)

    def get_relationship_fields(self) -> set[str]:
        relationship_fields = set()
        properties = self.schema().get("properties")

        for key, value in properties.items():
            if value.get("$ref"):
                field_value = getattr(self, key)
                result = issubclass(field_value.__class__, (ModelBase, BaseModel))

                if result:
                    relationship_fields.add(key)
        return relationship_fields

    @classmethod
    def from_model(cls, model: BaseModel):
        return cls(**model.dict())

    class Config(object):
        orm_mode = True
        validate_assignment = True


class UpdateBase(ModelBase):
    id: int

    def __init__(self, **data):
        super().__init__(**data)
        field_data = copy.deepcopy(data)
        field_data.pop("id", None)
        if not any(field_data.values()):
            raise MissDataError("At least one field should have a value in Put method")
