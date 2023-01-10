from newspy.models import Publication
from newspy.newsapi.client import NewsapiClient, NewsapiEndpoint
from newspy.shared.http_client import HttpClient


class Newspy:
    def __init__(self, newsapi_key: str) -> None:
        self._newsapi_key = newsapi_key

    def publications(self) -> list[Publication]:
        newsapi_client = NewsapiClient(http_client=HttpClient(), api_key=self._newsapi_key)

        return newsapi_client.publications(
            endpoint=NewsapiEndpoint.TOP_HEADLINES
        )
