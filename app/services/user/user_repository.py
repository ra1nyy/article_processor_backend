from sqlalchemy import select

from app.database.base_repository import BaseRepository
from app.database.entities import UserEntity
from app.models import UserRaw


class UserRepository(BaseRepository[UserRaw]):
    model = UserRaw
    entity = UserEntity

    async def get_by_username(self, username: str) -> UserRaw | None:
        async with self.db_session() as session:
            query = select(UserEntity).limit(1).where(UserEntity.username == username)
            entity = await session.execute(query)
            entity = entity.scalar()
            if not entity:
                return None

            return entity.to_model()
