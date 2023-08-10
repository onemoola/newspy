import os

default_client_config = {}


def configure(newsorg_api_key: str | None = None) -> None:
    global default_client_config

    if newsorg_api_key is None:
        newsorg_api_key = os.getenv("NEWSORG_API_KEY")

    default_client_config = {
        "newsorg_api_key": newsorg_api_key,
    }
