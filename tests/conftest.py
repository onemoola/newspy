import json

import pytest

from newspy.newsapi.models import NewsapiArticle, NewsapiArticlesRes, Source
from newspy.shared.http_client import HttpMethod


# noinspection PyMethodMayBeStatic
class HttpClientMock:
    def _build_session(self) -> None:
        return None

    def send(
        self,
        method: HttpMethod,
        url: str,
        headers: dict | None = None,
        params: dict | None = None,
        payload: dict | None = None,
    ) -> json:
        return {
            "status": "ok",
            "totalResults": 86,
            "articles": [
                {
                    "source": {"id": "fortune", "name": "Fortune"},
                    "author": "Emma Hinchliffe, Paige McGlauflin",
                    "title": "Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
                    "description": "Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
                    "url": "https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
                    "urlToImage": "https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
                    "publishedAt": "2022-06-01T13:22:34Z",
                    "content": "Skip to Content",
                }
            ],
        }


@pytest.fixture
def newsapi_article_source() -> Source:
    return Source(id="fortune", name="Fortune")


@pytest.fixture
def newsapi_article(newsapi_article_source) -> NewsapiArticle:
    return NewsapiArticle(
        source=newsapi_article_source,
        author="Emma Hinchliffe, Paige McGlauflin",
        title="Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
        description="Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
        url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
        urlToImage="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
        publishedAt="2022-06-01T13:22:34Z",
        content="Skip to Content",
    )


@pytest.fixture
def newsapi_articles_res(newsapi_article) -> NewsapiArticlesRes:
    return NewsapiArticlesRes(status="ok", totalResults=86, articles=[newsapi_article])


@pytest.fixture
def newsapi_article_res_json() -> json:
    return json.dumps(
        {
            "status": "ok",
            "totalResults": 86,
            "articles": [
                {
                    "source": {"id": "fortune", "name": "Fortune"},
                    "author": "Emma Hinchliffe, Paige McGlauflin",
                    "title": "Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
                    "description": "Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, a resource hub for working mothers aiming to prevent mid-career drop-off.",
                    "url": "https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
                    "urlToImage": "https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
                    "publishedAt": "2022-06-01T13:22:34Z",
                    "content": "Skip to Content",
                }
            ],
        }
    )
