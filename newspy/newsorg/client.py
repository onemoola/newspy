import logging
from enum import Enum

from newspy.client import default_client_config
from newspy.shared.models import Language, Country
from newspy.newsorg.models import (
    NewsorgArticlesRes,
    NewsorgCategory,
    NewsorgSourceRes,
    NewsorgSource,
    NewsorgArticle,
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient, HttpMethod

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2"


class NewsorgEndpoint(str, Enum):
    EVERYTHING = "EVERYTHING"
    TOP_HEADLINES = "TOP_HEADLINES"
    SOURCES = "SOURCES"


def create_newsorg_url(endpoint: NewsorgEndpoint) -> str:
    match endpoint:
        case NewsorgEndpoint.EVERYTHING:
            return f"{BASE_URL}/everything"
        case NewsorgEndpoint.TOP_HEADLINES:
            return f"{BASE_URL}/top-headlines"
        case NewsorgEndpoint.SOURCES:
            return f"{BASE_URL}/top-headlines/sources"
        case _:
            raise NewspyException(
                msg=f"The endpoint has to be one of the following values: 'EVERYTHING' or 'TOP_HEADLINES' or 'SOURCES'",
            )


def _create_params(page_size: int = 100, page: int = 1) -> dict[str, str]:
    newsorg_api_key = default_client_config.get("newsorg_api_key")

    if newsorg_api_key is None:
        raise NewspyException(
            msg="The Newsorg API key is not configured. Please configure it by calling the configure function.",
        )

    return {"apiKey": newsorg_api_key, "pageSize": page_size, "page": page}


def get_articles(
    endpoint: NewsorgEndpoint = NewsorgEndpoint.TOP_HEADLINES,
    search_text: str | None = None,
    category: NewsorgCategory | None = None,
    country: Country | None = None,
    sources: list[NewsorgSource] | None = None,
) -> list[NewsorgArticle]:
    params = _create_params()

    if category and sources:
        raise NewspyException(
            msg="Choose either the category and sources attributes. Not both.",
        )

    if search_text:
        params["q"] = search_text
    if category and endpoint == NewsorgEndpoint.TOP_HEADLINES:
        params["category"] = category.name
    if country and endpoint == NewsorgEndpoint.TOP_HEADLINES:
        params["country"] = country.name
    if sources and len(sources) > 0:
        params["sources"] = ",".join([source.id for source in sources])

    http_client = HttpClient()
    resp_json = http_client.send(
        method=HttpMethod.GET,
        url=create_newsorg_url(endpoint=endpoint),
        params=params,
    )

    try:
        article_res = NewsorgArticlesRes(**resp_json)
    except TypeError as err:
        raise NewspyException(
            msg=f"Failed to validate the News Org articles response json: {resp_json}",
            reason=str(err),
        )

    return article_res.articles


def get_sources(
    category: NewsorgCategory | None = None,
    language: Language | None = None,
    country: Country | None = None,
) -> list[NewsorgSource]:
    params = _create_params()

    if category:
        params["category"] = category.value
    if language:
        params["language"] = language.value
    if country:
        params["country"] = country.value

    http_client = HttpClient()
    resp_json = http_client.send(
        method=HttpMethod.GET,
        url=create_newsorg_url(endpoint=NewsorgEndpoint.SOURCES),
        params=params,
    )

    try:
        source_res = NewsorgSourceRes(**resp_json)
    except TypeError as type_error:
        raise NewspyException(
            msg=f"Failed to validate the News Org sources response json: {resp_json}",
            reason=str(type_error),
        )

    return source_res.sources
