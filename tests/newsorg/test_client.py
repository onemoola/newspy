from datetime import datetime, timezone

import pytest

from newspy.newsorg.client import create_url, NewsorgEndpoint, NewsorgClient
from newspy.newsorg.models import (
    NewsorgCategory,
    Source,
    Publisher,
    Publication,
)
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient
from tests.conftest import HttpClientMock

API_KEY = "seckfkdLkkekeKy"


def test_create_url_when_endpoint_is_everything() -> None:
    expected = "https://newsapi.org/v2/everything"
    actual = create_url(endpoint=NewsorgEndpoint.EVERYTHING)

    assert actual == expected


def test_create_url_when_endpoint_is_top_headlines() -> None:
    expected = "https://newsapi.org/v2/top-headlines"
    actual = create_url(endpoint=NewsorgEndpoint.TOP_HEADLINES)

    assert actual == expected


def test_create_url_when_endpoint_is_sources() -> None:
    expected = "https://newsapi.org/v2/top-headlines/sources"
    actual = create_url(endpoint=NewsorgEndpoint.SOURCES)

    assert actual == expected


def test_create_url_when_endpoint_is_not_recognised() -> None:
    with pytest.raises(NewspyException):
        create_url(endpoint="something-else")


def test_publications_when_category_and_sources_are_not_none() -> None:
    with pytest.raises(NewspyException):
        newsorg_client = NewsorgClient(http_client=HttpClient(), api_key=API_KEY)
        newsorg_client.publications(
            endpoint=NewsorgEndpoint.EVERYTHING,
            search_text="bitcoin",
            category=NewsorgCategory.BUSINESS,
            sources=[Source(id="news-org", name="News Organisation")],
        )


def test_publications_by_sources() -> None:
    expected = [
        Publication(
            slug="fortune-why-a-former-softbank-partner-is-tackling-midcareer-dropoff-for-working-mothers",
            url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
            url_to_image="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
            title="Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
            abstract="Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
            author="Emma Hinchliffe, Paige McGlauflin",
            publisher=Publisher(id="fortune", name="Fortune"),
            published=datetime(2022, 6, 1, 13, 22, 34, tzinfo=timezone.utc),
        )
    ]

    newsorg_client = NewsorgClient(http_client=HttpClientMock(), api_key=API_KEY)
    actual = newsorg_client.publications(
        endpoint=NewsorgEndpoint.EVERYTHING,
        search_text="bitcoin",
        sources=[
            Source(id="bloomberg", name="Bloomberg"),
            Source(id="business-insider", name="Business Insider"),
        ],
    )

    assert actual == expected
