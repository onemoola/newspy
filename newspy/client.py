import os

from newspy.shared.models import Publication
from newspy.newsorg.client import NewsorgClient, NewsorgEndpoint
from newspy.newsorg.models import NewsorgCategory
from newspy.shared.http_client import HttpClient


default_client_config = {}


def configure(newsorg_api_key: str | None = None) -> None:
    global default_client_config

    if newsorg_api_key is None:
        newsorg_api_key = os.getenv("NEWSORG_API_KEY")

    default_client_config = {
        "newsorg_api_key": newsorg_api_key,
    }


class Newspy:
    def __init__(self, newsorg_key: str) -> None:
        self._newsorg_key = newsorg_key

    def get_publications(self) -> list[Publication]:
        newsorg_client = NewsorgClient(
            http_client=HttpClient(), api_key=self._newsorg_key
        )

        newsorg_articles = newsorg_client.get_articles(
            endpoint=NewsorgEndpoint.TOP_HEADLINES, category=NewsorgCategory.BUSINESS
        )

        return [article.to_publication() for article in newsorg_articles]
