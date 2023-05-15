from app.services.auth.auth_respository import AuthRepository
from app.services.auth.auth_service import AuthService


def get_auth_service(providers, session, user_service, config, logger):
    auth_repository = providers.Factory(
        AuthRepository,
        db_session=session,
    )

    return providers.Factory(
        AuthService,
        config=config,
        repository=auth_repository,
        user_service=user_service,
        logger=logger,
    )
