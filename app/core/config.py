from pydantic import BaseModel

from app.utils.env_utils import load_config


class Config(BaseModel):
    root_path: str
    routers_root_path: str

    db_url: str
    db_url_test: str

    logger_level: str = "INFO"
    graylog_host: str = None
    graylog_port: int = None
    graylog_facility: str = None
    developer_logger: bool = None

    developer_mode: bool
    debug: bool
    uvicorn_server_port: int

    session_expired_minutes: int
    refresh_token_expired_days: int

    default_items_on_page: int = 10

    development_routers: bool = False

    formatted_docs_path: str = None
    attached_docs_path: str = None

    @classmethod
    def load_config(cls) -> "Config":
        data_env = load_config()
        return Config(
            root_path=data_env.get("ROOT_PATH", "/api"),
            routers_root_path=data_env.get("ROUTERS_ROOT_PATH", ""),
            db_url=data_env["DB_URL"],
            db_url_test=data_env["DB_URL_TEST"],
            graylog_host=data_env.get("GRAYLOG_HOST"),
            graylog_port=data_env.get("GRAYLOG_PORT"),
            graylog_facility=data_env.get("GRAYLOG_FACILITY"),
            logger_level=data_env.get("LOGGER_LEVEL", "INFO"),
            developer_logger=cls.__check_true(data_env.get("DEVELOPER_LOGGER", False)),
            developer_mode=cls.__check_true(data_env.get("DEVELOPER_MODE")),
            debug=cls.__check_true(data_env.get("DEBUG")),
            uvicorn_server_port=data_env.get("UVICORN_SERVER_PORT", 3000),
            session_expired_minutes=data_env.get("SESSION_EXPIRED_MINUTES", 15),
            refresh_token_expired_days=data_env.get("REFRESH_TOKEN_EXPIRED_DAYS", 3),
            default_items_on_page=data_env.get("DEFAULT_ITEMS_ON_PAGE", 10),
            development_routers=cls.__check_true(value=data_env.get("DEVELOPMENT_ROUTERS", False)),

            formatted_docs_path=data_env.get('FORMATTED_DOCS_PATH'),
            attached_docs_path=data_env.get('ATTACHED_DOCS_PATH')
        )

    @staticmethod
    def __check_true(value) -> bool:
        return str(value).lower() == "true"


config = Config.load_config()


def get_config():
    return config
