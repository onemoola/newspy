import logging
from enum import Enum

from newspy.models import Language, Country
from newspy.newsapi.models import (
    Publication,
    NewsapiArticlesRes,
    NewsapiCategory,
    NewsapiArticleSourceRes,
    Source,
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient, HttpMethod

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2"


class NewsapiEndpoint(str, Enum):
    EVERYTHING = "EVERYTHING"
    TOP_HEADLINES = "TOP_HEADLINES"
    SOURCES = "SOURCES"


def create_url(endpoint: NewsapiEndpoint) -> str:
    match endpoint:
        case NewsapiEndpoint.EVERYTHING:
            return f"{BASE_URL}/everything"
        case NewsapiEndpoint.TOP_HEADLINES:
            return f"{BASE_URL}/top-headlines"
        case NewsapiEndpoint.SOURCES:
            return f"{BASE_URL}/top-headlines/sources"
        case _:
            raise NewspyException(
                msg=f"The endpoint has to be one of the following values: 'EVERYTHING' or 'TOP_HEADLINES' or 'SOURCES'",
            )


class NewsapiClient:
    def __init__(self, http_client: HttpClient, api_key: str) -> None:
        self._http_client = http_client
        self._api_key = api_key

    def publications(
        self,
        endpoint: NewsapiEndpoint,
        search_text: str | None = None,
        category: NewsapiCategory | None = None,
        country: Country | None = None,
        sources: list[Source] | None = None,
    ) -> list[Publication]:
        if category and sources:
            raise NewspyException(
                msg="Choose either the category and sources attributes. Not both.",
            )

        params = {"apiKey": self._api_key, "pageSize": 100, "page": 1}

        if search_text:
            params["q"] = search_text
        if category and endpoint == NewsapiEndpoint.TOP_HEADLINES:
            params["category"] = category.value
        if country and endpoint == NewsapiEndpoint.TOP_HEADLINES:
            params["country"] = country.value
        if sources and len(sources) > 0:
            params["sources"] = ",".join([source.id for source in sources])

        resp_json = self._http_client.send(
            method=HttpMethod.GET, url=create_url(endpoint=endpoint), params=params
        )

        try:
            article_res = NewsapiArticlesRes(**resp_json)
        except TypeError as type_error:
            raise NewspyException(
                msg=f"Failed to validate the News Org articles response json: {resp_json}",
                reason=str(type_error),
            )

        return [article.to_publication() for article in article_res.articles]

    def sources(
        self,
        endpoint=NewsapiEndpoint.SOURCES,
        category: NewsapiCategory | None = None,
        language: Language | None = None,
        country: Country | None = None,
    ) -> list[Source]:
        params = {"apiKey": self._api_key}

        if category:
            params["category"] = category.value
        if language:
            params["language"] = language.value
        if country:
            params["country"] = country.value

        resp_json = self._http_client.send(
            method=HttpMethod.GET, url=create_url(endpoint=endpoint), params=params
        )

        try:
            return NewsapiArticleSourceRes(**resp_json).sources
        except TypeError as type_error:
            raise NewspyException(
                msg=f"Failed to validate the News Org sources response json: {resp_json}",
                reason=str(type_error),
            )
