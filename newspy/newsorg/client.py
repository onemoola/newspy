import logging
from datetime import date

from newspy import client
from newspy.models import Country, Language, Category
from newspy.newsorg.models import (
    NewsorgArticlesRes,
    NewsorgSourceRes,
    NewsorgSource,
    NewsorgArticle,
    NewsorgEndpoint,
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient, HttpMethod

logger = logging.getLogger(__name__)

BASE_URL = "https://newsapi.org/v2"


def create_url(endpoint: NewsorgEndpoint) -> str:
    match endpoint:
        case NewsorgEndpoint.EVERYTHING:
            return f"{BASE_URL}/everything"
        case NewsorgEndpoint.TOP_HEADLINES:
            return f"{BASE_URL}/top-headlines"
        case _:
            raise NewspyException(
                msg=f"The endpoint has to be one of the following values: 'EVERYTHING' or 'TOP_HEADLINES' or 'SOURCES'",
            )


def create_articles_params(
    endpoint: NewsorgEndpoint = NewsorgEndpoint.TOP_HEADLINES,
    search_text: str | None = None,
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
    sources: list[NewsorgSource] | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    page_size: int | None = None,
    page: int | None = None,
) -> dict[str, str]:
    newsorg_api_key = client.default_client_config.get("newsorg_api_key")

    if newsorg_api_key is None:
        raise NewspyException(
            msg="The Newsorg API key is not configured. Please configure it by calling the configure function.",
        )

    if category and sources:
        raise NewspyException(
            msg="Choose either the category and sources attributes. Not both.",
        )

    params = {"apiKey": newsorg_api_key}

    if language:
        params["language"] = language.value
    if search_text:
        params["q"] = search_text
    if sources and len(sources) > 0:
        params["sources"] = ",".join([source.id for source in sources])

    if endpoint.TOP_HEADLINES:
        if not search_text and not language and not country and not category:
            raise NewspyException(
                msg="The search text, country, or category attribute is required for the TOP_HEADLINES endpoint.",
            )

        if country:
            params["country"] = country.value

        if category:
            params["category"] = category.value

    if endpoint.EVERYTHING:
        if from_date and to_date:
            if from_date > to_date:
                raise NewspyException(
                    msg="The from date cannot be greater than the to date.",
                )

            params["from"] = from_date.strftime("%Y-%m-%d")
            params["to"] = to_date.strftime("%Y-%m-%d")

    if not page_size:
        page_size = 100
    params["pageSize"] = page_size

    if not page:
        page = 1
    params["page"] = page

    return params


def create_sources_params(
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
) -> dict[str, str]:
    newsorg_api_key = client.default_client_config.get("newsorg_api_key")

    if newsorg_api_key is None:
        raise NewspyException(
            msg="The Newsorg API key is not configured. Please configure it by calling the configure function.",
        )

    params = {"apiKey": newsorg_api_key}

    if category:
        params["category"] = category.value
    if country:
        params["country"] = country.value
    if language:
        params["language"] = language.value

    return params


def get_articles(
    endpoint: NewsorgEndpoint = NewsorgEndpoint.TOP_HEADLINES,
    search_text: str | None = None,
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
    sources: list[NewsorgSource] | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    page_size: int | None = None,
    page: int | None = None,
) -> list[NewsorgArticle]:
    params = create_articles_params(
        endpoint=endpoint,
        search_text=search_text,
        category=category,
        country=country,
        language=language,
        sources=sources,
        from_date=from_date,
        to_date=to_date,
        page_size=page_size,
        page=page,
    )

    http_client = HttpClient()
    resp_json = http_client.send(
        method=HttpMethod.GET,
        url=create_url(endpoint=endpoint),
        params=params,
    )

    try:
        article_res = NewsorgArticlesRes(**resp_json)
    except TypeError as exc:
        raise NewspyException(
            msg=f"Failed to validate the News Org articles response json: {resp_json}",
            reason=str(exc),
        )

    return article_res.articles


def get_sources(
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
) -> list[NewsorgSource]:
    params = create_sources_params(
        category=category, language=language, country=country
    )

    http_client = HttpClient()
    resp_json = http_client.send(
        method=HttpMethod.GET,
        url=f"{BASE_URL}/top-headlines/sources",
        params=params,
    )

    try:
        source_res = NewsorgSourceRes(**resp_json)
    except TypeError as exc:
        raise NewspyException(
            msg=f"Failed to validate the News Org sources response json: {resp_json}",
            reason=str(exc),
        )

    return source_res.sources
