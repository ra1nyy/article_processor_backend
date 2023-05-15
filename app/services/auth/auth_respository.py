import datetime

from sqlalchemy import func, select, update

from app.database.entities import UserSessionEntity
from app.models import UserSession


class AuthRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def create_session(self, model: UserSession) -> UserSession:
        async with self.db_session() as session:
            entity = UserSessionEntity.from_model(model)
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
        return entity.to_model()

    async def get_session(self, token_key: str) -> UserSession | None:
        async with self.db_session() as session:
            query = (
                select(UserSessionEntity)
                .limit(1)
                .where(
                    UserSessionEntity.token == token_key,
                    UserSessionEntity.token_expired_at >= datetime.datetime.utcnow(),
                )
            )
            entity = await session.scalar(query)
        if not entity:
            return None
        return entity.to_model()

    async def get_session_by_refresh_token(self, refresh_token) -> UserSession | None:
        async with self.db_session() as session:
            query = (
                select(UserSessionEntity)
                .limit(1)
                .where(
                    UserSessionEntity.refresh_token == refresh_token,
                    UserSessionEntity.refresh_token_expired_at >= func.now(),
                )
            )
            entity = await session.scalar(query)
        if not entity:
            return None
        return entity.to_model()

    async def update_session(self, session_model: UserSession) -> UserSession:
        async with self.db_session() as session:
            await session.execute(
                update(UserSessionEntity)
                .where(UserSessionEntity.id == session_model.id)
                .values(session_model.dict()),
            )
            await session.commit()
            return await self.get_session(session_model.token)
