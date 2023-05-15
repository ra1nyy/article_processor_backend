import uvicorn

from app.api.server import create_api_server
from app.core.config import Config
from app.core.containers import wire_modules

app = create_api_server()
wire_modules()

config = Config.load_config()
is_developer_mode = config.developer_mode

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=config.uvicorn_server_port,
        reload=config.developer_mode,
    )
