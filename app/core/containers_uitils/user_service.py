from app.services.user.user_repository import UserRepository
from app.services.user.user_service import UserService


def get_user_service(providers, session, config, logger):
    user_repository = providers.Factory(
        UserRepository,
        db_session=session,
    )

    return providers.Factory(
        UserService,
        repository=user_repository,
        config=config,
        logger=logger,
    )
