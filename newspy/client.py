from newspy.models import Publication
from newspy.newsorg.client import NewsorgClient, NewsorgEndpoint
from newspy.shared.http_client import HttpClient


class Newspy:
    def __init__(self, newsorg_key: str) -> None:
        self._newsorg_key = newsorg_key

    def publications(self) -> list[Publication]:
        newsorg_client = NewsorgClient(
            http_client=HttpClient(), api_key=self._newsorg_key
        )

        return newsorg_client.publications(endpoint=NewsorgEndpoint.TOP_HEADLINES)
