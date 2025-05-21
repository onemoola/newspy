import asyncio # Added
from datetime import date
from unittest.mock import AsyncMock, patch # Added

import pytest
# import responses # Commented out, will remove if all relevant tests are async
from newspy import client # Used for configure, keep
from newspy import newsorg
from newspy.models import Language, Country, Category
from newspy.newsorg.models import ( # Added NewsorgArticlesRes, NewsorgSourceRes
    NewsorgSource, NewsorgArticle, NewsorgEndpoint, NewsorgArticlesRes, NewsorgSourceRes
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient # Added for mocking

API_KEY = "seckfkdLkkekeKy"
BASE_URL = "https://newsapi.org/v2" # Kept for existing sync tests if any, or for reference

# Mark tests in this file as asyncio if most become async.
# For focused changes, can mark individual tests.
pytestmark = pytest.mark.asyncio # Apply to all tests in this file

@pytest.fixture
def mock_http_client():
    """Provides a mock HttpClient instance for dependency injection."""
    client = AsyncMock(spec=HttpClient)
    return client

# Synchronous tests for utility functions can remain as they are.
def test_create_url_when_endpoint_is_everything() -> None:
    expected = "https://newsapi.org/v2/everything"
    actual = newsorg.create_url(endpoint=NewsorgEndpoint.EVERYTHING)

    assert actual == expected


def test_create_url_when_endpoint_is_top_headlines() -> None:
    expected = "https://newsapi.org/v2/top-headlines"
    actual = newsorg.create_url(endpoint=NewsorgEndpoint.TOP_HEADLINES)

    assert actual == expected


def test_create_url_when_endpoint_is_not_recognised() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_url(endpoint="something-else")  # type: ignore


def test_articles_when_category_and_sources_are_not_none() -> None:
    # This test is for a synchronous part of the client (raising an exception before any async call)
    # However, get_articles itself is now async. So this test needs to be async.
    client.configure(newsorg_api_key=API_KEY) # Ensure API key is configured for param creation
    with pytest.raises(NewspyException):
        # Even though it raises early, call it with await since it's an async function
        await newsorg.get_articles(
            endpoint=NewsorgEndpoint.EVERYTHING,
            search_text="bitcoin",
            category=Category.BUSINESS,
            sources=[NewsorgSource(id="news-org", name="News Organisation")],
            http_client=mock_http_client() # Pass a mock client
        )


def test_create_articles_params_when_endpoint_is_top_headlines() -> None:
    expected = {
        "apiKey": API_KEY,
        "q": "bitcoin",
        "category": "business",
        "country": "us",
        "language": "en",
        "pageSize": 100,
        "page": 1,
    }

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_articles_params(
        endpoint=NewsorgEndpoint.TOP_HEADLINES,
        search_text="bitcoin",
        category=Category.BUSINESS,
        country=Country.US,
        language=Language.EN,
        page_size=100,
        page=1,
    )

    assert actual == expected


def test_create_articles_params_when_endpoint_is_top_headlines_when_all_params_are_none() -> (
    None
):
    with pytest.raises(NewspyException):
        newsorg.create_articles_params(endpoint=NewsorgEndpoint.TOP_HEADLINES)


def test_create_articles_params_when_newsorg_api_key_is_none() -> None:
    client.configure(newsorg_api_key=None)

    with pytest.raises(NewspyException):
        newsorg.create_articles_params(
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
        )


def test_create_articles_params_when_category_and_sources_are_not_none() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_articles_params(
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
            category=Category.BUSINESS,
            sources=[NewsorgSource(id="news-org", name="News Organisation")],
        )


def test_create_articles_params_when_country_and_sources_are_not_none() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_articles_params(
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
            country=Country.US,
            sources=[NewsorgSource(id="news-org", name="News Organisation")],
        )


def test_create_articles_params_when_endpoint_is_not_recognised() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_articles_params(
            endpoint="something-else",  # type: ignore
            search_text="bitcoin",
        )


def test_create_articles_params_when_endpoint_is_everything() -> None:
    expected = {
        "apiKey": API_KEY,
        "q": "bitcoin",
        "pageSize": 100,
        "page": 1,
        "sources": "news-org",
        "from": "2021-01-01",
        "to": "2021-01-02",
        "language": "en",
    }

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_articles_params(
        endpoint=NewsorgEndpoint.EVERYTHING,
        search_text="bitcoin",
        sources=[NewsorgSource(id="news-org", name="News Organisation")],
        from_date=date(2021, 1, 1),
        to_date=date(2021, 1, 2),
        language=Language.EN,
    )

    assert actual == expected


def test_create_articles_params_when_endpoint_is_everything_and_page_size_and_page_are_not_none() -> (
    None
):
    expected = {
        "apiKey": API_KEY,
        "q": "bitcoin",
        "sources": "news-org",
        "from": "2021-01-01",
        "to": "2021-01-02",
        "pageSize": 100,
        "page": 1,
    }

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_articles_params(
        endpoint=NewsorgEndpoint.EVERYTHING,
        search_text="bitcoin",
        sources=[NewsorgSource(id="news-org", name="News Organisation")],
        from_date=date(2021, 1, 1),
        to_date=date(2021, 1, 2),
        page_size=100,
        page=1,
    )

    assert actual == expected


def test_create_articles_params_when_endpoint_is_everything_and_page_size_and_page_are_none() -> (
    None
):
    expected = {
        "apiKey": API_KEY,
        "q": "bitcoin",
        "sources": "news-org",
        "from": "2021-01-01",
        "to": "2021-01-02",
        "pageSize": 100,
        "page": 1,
    }

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_articles_params(
        endpoint=NewsorgEndpoint.EVERYTHING,
        search_text="bitcoin",
        sources=[NewsorgSource(id="news-org", name="News Organisation")],
        from_date=date(2021, 1, 1),
        to_date=date(2021, 1, 2),
    )

    assert actual == expected


def test_create_articles_params_when_from_date_is_greater_than_to_date() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_articles_params(
            endpoint=NewsorgEndpoint.EVERYTHING,
            search_text="bitcoin",
            sources=[NewsorgSource(id="news-org", name="News Organisation")],
            from_date=date(2021, 1, 2),
            to_date=date(2021, 1, 1),
        )


def test_create_sources_params_when_all_params_are_none() -> None:
    expected = {"apiKey": API_KEY}

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_sources_params()

    assert actual == expected


def test_create_sources_params_when_newsorg_api_key_is_none() -> None:
    client.configure(newsorg_api_key=None)

    with pytest.raises(NewspyException):
        newsorg.create_sources_params()


def test_create_sources_params_when_language_is_not_none() -> None:
    expected = {"apiKey": API_KEY, "language": "en"}

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_sources_params(language=Language.EN)

    assert actual == expected


def test_create_sources_params_when_country_is_not_none() -> None:
    expected = {"apiKey": API_KEY, "country": "us"}

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_sources_params(country=Country.US)

    assert actual == expected


def test_create_sources_params_when_category_is_not_none() -> None:
    expected = {"apiKey": API_KEY, "category": "business"}

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.create_sources_params(category=Category.BUSINESS)

    assert actual == expected


# Keep newsorg_articles_res_json and newsorg_sources_res_json if they are from conftest and return dicts
async def test_get_newsorg_articles_async(mock_http_client, newsorg_articles_res_json_dict):
    # newsorg_articles_res_json_dict should be a fixture returning the JSON as a Python dict
    mock_http_client.send.return_value = newsorg_articles_res_json_dict 
    client.configure(newsorg_api_key=API_KEY) # For param creation

    expected_article = NewsorgArticle(
        source=NewsorgSource(name="Fortune", id="fortune"),
        author="Emma Hinchliffe, Paige McGlauflin",
        title="Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
        description="Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
        url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
        urlToImage="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
        publishedAt="2022-06-01T13:22:34Z",
        content="Skip to Content",
        archived_data=None 
    )
    
    actual_articles = await newsorg.get_articles(
        http_client=mock_http_client,
        endpoint=NewsorgEndpoint.TOP_HEADLINES,
        search_text="bitcoin", # Example search text
        sources=[NewsorgSource(id="fortune", name="Fortune")] # Ensure source matches whats in json
    )

    assert len(actual_articles) == 1
    # Compare relevant fields, as the mock_http_client won't do full Pydantic parsing from raw JSON
    assert actual_articles[0].title == expected_article.title
    assert actual_articles[0].url == expected_article.url
    assert actual_articles[0].source.id == expected_article.source.id
    
    # Verify http_client.send was called (details depend on how params are created and passed)
    mock_http_client.send.assert_called_once()


async def test_get_newsorg_articles_exception_async(mock_http_client):
    mock_http_client.send.return_value = {"status": "ok", "totalResults": 1, "articles": [{"source": {"id": "foo", "name": "bar"}, "title": "t", "description": "d", "url": "u", "urlToImage": "i", "publishedAt": "p", "content": "c", "unexpected_field": "error here"}]}
    client.configure(newsorg_api_key=API_KEY)

    with pytest.raises(NewspyException) as excinfo:
        await newsorg.get_articles(
            http_client=mock_http_client,
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin"
        )
    assert "Failed to validate the News Org articles response json" in str(excinfo.value)
    assert "unexpected keyword argument 'unexpected_field'" in str(excinfo.value)


async def test_get_newsorg_sources_async(mock_http_client, newsorg_sources_res_json_dict):
    # newsorg_sources_res_json_dict should be a fixture returning the JSON as a Python dict
    mock_http_client.send.return_value = newsorg_sources_res_json_dict
    client.configure(newsorg_api_key=API_KEY)

    expected_source = NewsorgSource(
        id="abc-news",
        name="ABC News",
        description="Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com.",
        url="https://abcnews.go.com",
        category=Category.GENERAL,
        language=Language.EN,
        country=Country.US
    )

    actual_sources = await newsorg.get_sources(
        http_client=mock_http_client,
        category=Category.GENERAL, 
        language=Language.EN, 
        country=Country.US
    )
    
    assert len(actual_sources) == 1
    assert actual_sources[0] == expected_source
    mock_http_client.send.assert_called_once()


async def test_get_newsorg_articles_with_archived_data(mock_http_client, newsorg_articles_res_json_dict):
    mock_http_client.send.return_value = newsorg_articles_res_json_dict
    client.configure(newsorg_api_key=API_KEY)

    mock_archived_content = {"status": "success", "title": "Archived Title", "text": "Archived text."}

    # Patch fetch_from_archivemd in the newsorg.client module
    with patch("newspy.newsorg.client.fetch_from_archivemd", AsyncMock(return_value=mock_archived_content)) as mock_fetch_archive:
        articles = await newsorg.get_articles(
            http_client=mock_http_client,
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
            sources=[NewsorgSource(id="fortune", name="Fortune")], # Matches fixture
            fetch_archived=True
        )

    assert len(articles) > 0
    first_article = articles[0]
    assert first_article.archived_data is not None
    assert first_article.archived_data["title"] == "Archived Title"
    
    # Ensure fetch_from_archivemd was called for each article URL
    # Based on newsorg_articles_res_json, there's one article.
    # If newsorg_articles_res_json_dict yields multiple articles, this needs adjustment.
    # For this example, assume one article for simplicity or adjust if fixture has more.
    expected_article_url_from_fixture = "https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/"
    mock_fetch_archive.assert_called_once_with(expected_article_url_from_fixture, mock_http_client)


async def test_get_newsorg_articles_with_archived_data_fetch_fails(mock_http_client, newsorg_articles_res_json_dict):
    mock_http_client.send.return_value = newsorg_articles_res_json_dict
    client.configure(newsorg_api_key=API_KEY)

    mock_archive_error = {"status": "failed", "error": "Archive fetch error"}
    with patch("newspy.newsorg.client.fetch_from_archivemd", AsyncMock(return_value=mock_archive_error)) as mock_fetch_archive:
        articles = await newsorg.get_articles(
            http_client=mock_http_client,
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
            sources=[NewsorgSource(id="fortune", name="Fortune")],
            fetch_archived=True
        )
    
    assert len(articles) > 0
    first_article = articles[0]
    assert first_article.archived_data is not None
    assert first_article.archived_data["status"] == "failed"
    assert "Archive fetch error" in first_article.archived_data["error"]


async def test_get_newsorg_sources_exception_async(mock_http_client):
    # Simulate a broken JSON structure that would cause a TypeError during Pydantic validation
    mock_http_client.send.return_value = {"status": "ok", "sources": [{"id": "abc-news", "unexpected_field": "error here"}]}
    client.configure(newsorg_api_key=API_KEY)

    with pytest.raises(NewspyException) as excinfo:
        await newsorg.get_sources(
            http_client=mock_http_client,
            category=Category.GENERAL, language=Language.EN, country=Country.US
        )
    assert "Failed to validate the News Org sources response json" in str(excinfo.value)
    assert "unexpected keyword argument 'unexpected_field'" in str(excinfo.value)


# Note: The existing synchronous tests for create_url, create_articles_params, create_sources_params
# do not need to be async and can remain as they are, since they don't involve I/O.
# The tests using @responses.activate (like old test_get_newsorg_articles_by_sources, etc.)
# should be removed or fully converted to async with aiohttp mocking if they test async functions.
# For this refactoring, focus is on the async get_articles/get_sources and archive integration.
# The fixtures newsorg_articles_res_json and newsorg_sources_res_json from conftest.py
# are assumed to provide raw JSON strings. For the async tests, it's better if they
# provide Python dictionaries directly (e.g. newsorg_articles_res_json_dict).
# If they provide strings, the tests would need json.loads().
# I've assumed new fixtures like newsorg_articles_res_json_dict for clarity.
