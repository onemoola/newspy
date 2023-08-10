import pytest
import responses

from newspy import client
from newspy import newsorg, NewsorgEndpoint
from newspy.newsorg.models import (
    NewsorgCategory,
    NewsorgSource,
    NewsorgArticle,
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.models import Language, Country

API_KEY = "seckfkdLkkekeKy"
BASE_URL = "https://newsapi.org/v2/top-headlines"


def test_create_url_when_endpoint_is_everything() -> None:
    expected = "https://newsapi.org/v2/everything"
    actual = newsorg.create_url(endpoint=NewsorgEndpoint.EVERYTHING)

    assert actual == expected


def test_create_url_when_endpoint_is_top_headlines() -> None:
    expected = "https://newsapi.org/v2/top-headlines"
    actual = newsorg.create_url(endpoint=NewsorgEndpoint.TOP_HEADLINES)

    assert actual == expected


def test_create_url_when_endpoint_is_sources() -> None:
    expected = "https://newsapi.org/v2/top-headlines/sources"
    actual = newsorg.create_url(endpoint=NewsorgEndpoint.SOURCES)

    assert actual == expected


def test_create_url_when_endpoint_is_not_recognised() -> None:
    with pytest.raises(NewspyException):
        newsorg.create_url(endpoint="something-else")  # type: ignore


def test_publications_when_category_and_sources_are_not_none() -> None:
    with pytest.raises(NewspyException):
        newsorg.get_articles(
            endpoint=NewsorgEndpoint.EVERYTHING,
            search_text="bitcoin",
            category=NewsorgCategory.BUSINESS,
            sources=[NewsorgSource(id="news-org", name="News Organisation")],
        )


@responses.activate
def test_get_newsorg_articles_by_sources(newsorg_articles_res_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&pageSize=100&page=1&q=bitcoin&sources=bloomberg%2Cbusiness-insider",
            "body": newsorg_articles_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    expected = [
        NewsorgArticle(
            source=NewsorgSource(
                name="Fortune",
                id="fortune",
                description=None,
                url=None,
                category=None,
                language=None,
                country=None,
            ),
            author="Emma Hinchliffe, Paige McGlauflin",
            title="Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
            description="Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of "
            "Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
            url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working"
            "-mothers/",
            urlToImage="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
            publishedAt="2022-06-01T13:22:34Z",
            content="Skip to Content",
        )
    ]

    client.configure(newsorg_api_key=API_KEY)

    actual = newsorg.get_articles(
        endpoint=NewsorgEndpoint.TOP_HEADLINES,
        search_text="bitcoin",
        sources=[
            NewsorgSource(id="bloomberg", name="Bloomberg"),
            NewsorgSource(id="business-insider", name="Business Insider"),
        ],
    )

    assert actual == expected


@responses.activate
def test_get_newsorg_articles_exception(newsorg_articles_res_broken_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&pageSize=100&page=1&q=bitcoin&sources=bloomberg%2Cbusiness-insider",
            "body": newsorg_articles_res_broken_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    client.configure(newsorg_api_key=API_KEY)

    with pytest.raises(NewspyException) as exc:
        newsorg.get_articles(
            endpoint=NewsorgEndpoint.TOP_HEADLINES,
            search_text="bitcoin",
            sources=[
                NewsorgSource(id="bloomberg", name="Bloomberg"),
                NewsorgSource(id="business-insider", name="Business Insider"),
            ],
        )

    assert str(exc.value) == (
        "message: Failed to validate the News Org articles response json: {'status': "
        "0, 'totalResults': '86', 'articles': [{'source': {'id': 'fortune', 'name': "
        "'Fortune'}, 'author': 'Emma Hinchliffe, Paige McGlauflin', 'long_title': "
        "'Why a former SoftBank partner is tackling mid-career drop-off for working "
        "mothers', 'description': 'Former SoftBank partner and Facebook India "
        "director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for "
        "working mothers aiming to prevent mid-career drop-off.', 'url': "
        "'https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/', "
        "'urlToImage': "
        "'https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600', "
        "'publishedAt': '2022-06-01T13:22:34Z', 'content': 'Skip to Content'}]}, "
        "reason: NewsorgArticle.__init__() got an unexpected keyword argument "
        "'long_title'"
    )


@responses.activate
def test_get_newsorg_sources(newsorg_sources_res_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}/sources?apiKey={API_KEY}&category=general&language=en&country=us",
            "body": newsorg_sources_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    expected = [
        NewsorgSource(
            id="abc-news",
            name="ABC News",
            description="Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos "
            "at ABCNews.com.",
            url="https://abcnews.go.com",
            category=NewsorgCategory.GENERAL,
            language=Language.EN,
            country=Country.US,
        )
    ]

    client.configure(newsorg_api_key=API_KEY)
    actual = newsorg.get_sources(
        category=NewsorgCategory.GENERAL, language=Language.EN, country=Country.US
    )

    assert actual == expected


@responses.activate
def test_get_newsorg_source_exception(newsorg_sources_res_broken_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}/sources?apiKey={API_KEY}&category=general&language=en&country=us",
            "body": newsorg_sources_res_broken_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    client.configure(newsorg_api_key=API_KEY)

    with pytest.raises(NewspyException) as exc:
        newsorg.get_sources(
            category=NewsorgCategory.GENERAL, language=Language.EN, country=Country.US
        )

    assert str(exc.value) == (
        "message: Failed to validate the News Org sources response json: {'status': "
        "2, 'sources': [{'id': 'abc-news', 'full_name': 'ABC News', 'description': "
        "'Your trusted source for breaking news, analysis, exclusive interviews, "
        "headlines, and videos at ABCNews.com.', 'url': 'https://abcnews.go.com', "
        "'category': 'general', 'language': 'en', 'country': 'us'}]}, reason: "
        "NewsorgSource.__init__() got an unexpected keyword argument 'full_name'"
    )
