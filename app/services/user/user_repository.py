from sqlalchemy import select

from app.database.base_repository import BaseRepository
from app.database.entities import UserEntity
from app.models import UserRaw, User, UserRoleEnum


class UserRepository(BaseRepository[UserRaw]):
    model = UserRaw
    entity = UserEntity

    async def get_all_students(self):
        async with self.db_session() as session:
            query = select(UserEntity).where(UserEntity.role == UserRoleEnum.USER)
            result = await session.execute(query)
            return self.get_list(result.scalars())

    async def get_by_username(self, username: str) -> UserRaw | None:
        async with self.db_session() as session:

            query = select(UserEntity).limit(1).where(UserEntity.username == username)
            entity = await session.execute(query)

            entity = entity.scalar()
            if not entity:
                return None

            return entity.to_model()

    async def get_by_email(self, email: str) -> UserRaw | None:
        async with self.db_session() as session:

            query = select(UserEntity).limit(1).where(UserEntity.email == email)
            entity = await session.execute(query)

            entity = entity.scalar()
            if not entity:
                return None

            return entity.to_model()

    async def get_users_by_ids(self, user_ids: list):
        async with self.db_session() as session:
            result = await session.execute(
                select(UserEntity).where(
                    UserEntity.id.in_(user_ids),
                )
            )

            return self.get_list(result.scalars(), User)
