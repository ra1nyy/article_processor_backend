from app.api.errors import EntityNotFound
from app.models import User, UserRaw
from app.models.user.user_requests import UserUpdate
from app.services import BaseService
from app.services.user.user_repository import UserRepository


class UserService(BaseService[UserRaw]):
    model = UserRaw
    repository: UserRepository

    async def get_users(self) -> list[User]:
        return await self.repository.get_all()

    async def get_all_students(self) -> list[User]:
        return await self.repository.get_all_students()

    async def get_users_by_list_ids(self, list_ids: list) -> list[User]:
        users = await self.repository.get_users_by_ids(user_ids=list_ids)
        if not users:
            raise EntityNotFound('User')

        return users

    async def get_by_username(self, username: str) -> UserRaw | None:
        user = await self.repository.get_by_username(username)

        if not user:
            self.logger.exception('Entity "User" not found')
            raise EntityNotFound("User")
        return user

    async def get_by_id(self, user_id: int) -> UserRaw | None:
        return await self.repository.get_by_id(user_id)

    @BaseService.catch_db_error(entity=User.__name__, unique_field="username")
    async def update_user(
        self,
        update_user_request: UserUpdate,
        user_id: int,
    ) -> User:
        print(update_user_request.dict())
        update_user_request_with_id = UserUpdate(
            **update_user_request.dict(exclude={'id'}),
            id=user_id,
        )
        user = await self.repository.update(update_user_request_with_id)

        if not user:
            raise EntityNotFound("User")

        return user

    async def save(self, user: UserRaw | User):
        await self.repository.save(user)
