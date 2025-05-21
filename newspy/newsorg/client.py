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


async def get_articles(
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
    http_client: HttpClient | None = None,
    fetch_archived: bool = False,
) -> list[NewsorgArticle]:
    # This inner function will handle all fetching logic using a given client.
    async def _fetch_all_data_with_client(client_to_use: HttpClient) -> list[NewsorgArticle]:
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

        resp_json = await client_to_use.send(
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

        articles_list = article_res.articles

        if fetch_archived and articles_list:
            import asyncio # Ensure asyncio is imported
            from newspy.archiver import fetch_from_archivemd # Import here

            archive_fetch_tasks = [
                fetch_from_archivemd(article.url, client_to_use) for article in articles_list
            ]
            archived_results = await asyncio.gather(*archive_fetch_tasks, return_exceptions=True)

            for i, article in enumerate(articles_list):
                archived_data = archived_results[i]
                if isinstance(archived_data, Exception):
                    # Store error information if fetching archived data failed
                    article.archived_data = {"status": "failed", "error": str(archived_data)}
                else:
                    article.archived_data = archived_data
        
        return articles_list

    if http_client:
        return await _fetch_all_data_with_client(http_client)
    else:
        async with HttpClient() as client_instance:
            return await _fetch_all_data_with_client(client_instance)



async def get_sources(
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
    http_client: HttpClient | None = None,
) -> list[NewsorgSource]:
    params = create_sources_params(
        category=category, language=language, country=country
    )

    if http_client:
        resp_json = await http_client.send(
            method=HttpMethod.GET,
            url=f"{BASE_URL}/top-headlines/sources",
            params=params,
        )
    else:
        async with HttpClient() as client_instance:
            resp_json = await client_instance.send(
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
