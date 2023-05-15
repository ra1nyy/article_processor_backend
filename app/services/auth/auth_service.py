import uuid
from datetime import datetime, timedelta

from app.api.errors import ApiAccessError, EntityNotFound
from app.core.config import Config
from app.core.logger.appLogger import AppLogger
from app.models import Token, UserRaw, UserRoleEnum, UserSession, User
from app.services.auth.auth_respository import AuthRepository
from app.services.base_service import BaseService
from app.services.user.user_service import UserService


class AuthService(BaseService[User]):
    model = User
    repository: AuthRepository

    def __init__(
        self,
        config: Config,
        repository: AuthRepository,
        user_service: UserService,
        logger: AppLogger,
    ):
        super().__init__(config=config, repository=repository, logger=logger)
        self.user_service = user_service

    async def login(self, username: str, password: str, ip: str) -> Token:
        user = await self.user_service.get_by_username(username)

        if not user:
            self.logger.exception('Entity "User" not found')
            raise EntityNotFound("User")

        is_valid = user.validate_password(password)
        if not is_valid:
            self.logger.exception("access denied")
            raise ApiAccessError

        user.last_login = datetime.utcnow()
        await self.user_service.save(user)

        return await self.create_token(user.id, ip)

    async def refresh_token(self, refresh_token: str) -> Token:
        session: UserSession = await self.get_user_session_by_refresh_token(
            refresh_token,
        )
        if not session:
            self.logger.exception("access denied")
            raise ApiAccessError

        session.token = self.get_token_string()
        session.token_expired_at = self.get_expired_at()

        session = await self.repository.update_session(session)
        return Token.from_session(
            session=session,
            user_role=UserRoleEnum.USER,
            # TODO нужно доделать, чтобы роль бралась из ентити юзера
        )

    async def logout(self, token_key: str):
        session: UserSession = await self.get_user_session(token_key)
        if not session:
            return

        session.token_expired_at = datetime.now() - timedelta(seconds=1)
        await self.repository.update_session(session)

    async def get_user_session(self, token_key) -> UserSession | None:
        return await self.repository.get_session(token_key)

    async def get_user_session_by_refresh_token(
        self,
        refresh_token: str,
    ) -> UserSession | None:
        return await self.repository.get_session_by_refresh_token(refresh_token)

    async def get_user_by_session(self, session: UserSession) -> UserRaw | None:
        return await self.user_service.get_by_id(session.user_id)

    async def create_token(self, user_id: int, ip: str) -> Token:
        session = None
        session_exists = True
        while session_exists:
            token = self.get_token_string()
            refresh_token = self.get_token_string()
            session = UserSession(
                user_id=user_id,
                ip=ip,
                token=token,
                token_expired_at=self.get_expired_at(),
                refresh_token=refresh_token,
                refresh_token_expired_at=self.get_refresh_token_expired_at(),
            )
            session_exists = await self.is_session_exists(token, refresh_token)
        session = await self.repository.create_session(session)
        return Token.from_session(
            session,
            user_role=UserRoleEnum.USER,
        )

    async def is_session_exists(self, token: str, refresh_token: str) -> bool:
        session = await self.repository.get_session(token)
        if session:
            return True

        return not not await self.repository.get_session_by_refresh_token(
            refresh_token,
        )

    def get_expired_at(self):
        return datetime.utcnow() + timedelta(
            minutes=self.config.session_expired_minutes,
        )

    def get_refresh_token_expired_at(self):
        return datetime.utcnow() + timedelta(
            days=self.config.refresh_token_expired_days,
        )

    def get_token_string(self) -> str:
        return uuid.uuid4().hex
