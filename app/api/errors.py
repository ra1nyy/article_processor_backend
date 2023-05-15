from enum import Enum

from fastapi import HTTPException


class ApiNotFoundError(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "not found"


class ApiExistsError(HTTPException):
    def __init__(self):
        self.status_code = 409
        self.detail = "already exists"


class ApiAccessError(HTTPException):
    def __init__(self, message: str = None):
        self.status_code = 401
        self.detail = "access denied" + f". {message}" if message else None


class ApiPermissionError(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = "permission denied"


class ApiTechnicalError(HTTPException):
    def __init__(self):
        self.status_code = 500
        self.detail = "internal server error"


class AbsError(ApiTechnicalError):
    def __init__(self):
        self.name = ""
        self.detail = "abs method"


class WrongDataError(HTTPException):
    def __init__(self, loc="unk", message="field required"):
        self.status_code = 422
        self.loc = loc
        self.detail = [
            {
                "loc": (self.loc,),
                "msg": message,
                "type": "value_error",
            },
        ]


class InappropriateTypeOfWork(HTTPException):
    def __init__(self):
        self.status_code = 455
        self.detail = "collector_type_work is not appropriate for this operation"


class InappropriateEntities(HTTPException):
    def __init__(self, ids: set[int] = None):
        self.status_code = 456
        self.detail = (
            "entity are not appropriate for this operation(information in ids)"
        )
        self.ids = list(ids) if ids else []


class AdminChangingForbidden(HTTPException):
    def __init__(self):
        self.status_code = 458
        self.detail = "not enough permission to change admin entity"


class StatusIsForbidden(HTTPException):
    def __init__(self):
        self.status_code = 459
        self.detail = "inactive user status cannot change/set in this method"


class EntityCrossingAnotherEntity(HTTPException):
    def __init__(self, entity_name=None):
        entity_str = entity_name if entity_name else "entity"

        self.status_code = 460
        self.detail = f"this {entity_str} is crossing another exist {entity_str}"


class EntityNotFound(HTTPException):
    def __init__(self, entity_name: str = None):
        self.status_code = 461
        self.detail = (
            f'Entity{" "+entity_name if entity_name else ""} not found'  # noqa: WPS336
        )
        self.entity = entity_name


class NotAllowedEnumValue(HTTPException):
    def __init__(self, field_name, enum_values: list[Enum]):
        self.status_code = 463
        self.detail = f"{field_name} not in {enum_values}. " \
                      f"Only this values are valid for this method"


class DebtorsExistsError(HTTPException):
    def __init__(self):
        self.status_code = 464
        self.detail = "debtors exists"


class EntitiesBoundingError(HTTPException):
    """
    fields with information - 'first_entity',
    'first_entity_field', 'second_entity'.
    """

    def __init__(
        self,
        linking_entity: str,
        linking_entity_field: str,
        second_entity: str,
    ):
        self.status_code = 464
        self.detail = (
            f"{linking_entity}.{linking_entity_field} is not bound with {second_entity}"
        )

        self.first_entity = linking_entity
        self.first_entity_field = linking_entity_field
        self.second_entity = second_entity


class RouterPermissionError(HTTPException):
    def __init__(self, field_name: str = "some", entity_name: str = "some"):
        self.status_code = 465
        self.field_name = field_name
        self.entity_name = entity_name
        self.detail = (
            f"permission on this endpoint denied. "
            f"{entity_name.capitalize()}.{field_name} value is "
            f"inappropriate for this operation"
        )  # noqa: WPS318, WPS326, E501


class MissDataError(WrongDataError):
    def __init__(self, loc):
        super().__init__(loc=loc)


class EntityCreateError(HTTPException):
    def __init__(
        self,
        entity: str,
        unique_field: str | None = None,
        unique_entity_field_name: str | None = None,
    ):
        self.status_code = 466
        if unique_field is not None:
            self.detail = (
                f"{entity} with {unique_field} "
                f"'{unique_entity_field_name}' already exists"
            )
        else:
            self.detail = (
                f"Cannot create {entity} because smth is wrong with ForeignKey"
            )


class IncorrectServiceIntanse(HTTPException):
    def __init__(self, message: str = None):
        self.status_code = 467
        self.detail = message


class SeedingError(HTTPException):
    def __init__(self, message: str = None):
        self.status_code = 468
        self.detail = message
