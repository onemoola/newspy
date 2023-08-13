import json

import pytest
import responses

from newspy.newsorg.models import NewsorgArticlesRes
from newspy.shared import http_client
from newspy.shared.exceptions import NewspyHttpException
from newspy.shared.http_client import HttpClient, HttpMethod

API_KEY = "seckfkdLkkekeKy"

BASE_URL = "https://localhost/v2/top-headlines"
HEADERS = {
    "Content-Type": "application/json",
}
PARAMS = {
    "apiKey": API_KEY,
    "sources": "bloomberg,business-insider",
    "language": "en",
    "pageSize": 100,
}


@responses.activate
def test_http_client(newsorg_articles_res_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": newsorg_articles_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
    )

    article_res = NewsorgArticlesRes(**actual)
    assert article_res.status == "ok"
    assert article_res.totalResults == 86
    assert len(article_res.articles) == 1


@responses.activate
def test_http_client_when_http_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps({"error": {"message": "Bad request"}}),
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyHttpException):
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)


@responses.activate
def test_http_client_when_http_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps({"error": {"message": "Bad request"}}),
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyHttpException):
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)


@responses.activate
def test_http_client_when_server_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps({"error": {"message": "Bad request"}}),
            "status": 500,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyHttpException):
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)


@responses.activate
def test_http_client_when_value_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": {},
            "status": 200,
            "content_type": "application/json",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
    )

    assert actual is None


@responses.activate
def test_http_client_when_content_type_is_rss(rss_articles_res_xml) -> None:
    expected = [
        {
            "description": "Miami, Dubai and Singapore boom by welcoming those chased "
            "out of rival international hubs",
            "published": "Sun, 12 Mar 2023 13:00:35 GMT",
            "title": "Three global cities are pulling ahead since the peak of the "
            "pandemic",
            "url": "https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            "source_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        },
        {
            "description": "‘Lead white knight’ eyeing British arm of tech lender that "
            "had billions in deposits",
            "published": "Sun, 12 Mar 2023 12:54:53 GMT",
            "title": "UK seeks to tap Middle East money to buy out SVB unit",
            "url": "https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            "source_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        },
    ]

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://www.ft.com/?edition=international&format=rss",
            "body": rss_articles_res_xml,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.GET,
        url="https://www.ft.com/",
        headers={"Content-Type": "application/rss+xml"},
        params={"edition": "international", "format": "rss"},
    )

    assert actual == expected


def test_parse_xml() -> None:
    xml = """
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
            <channel>
                <title>
                    <![CDATA[ News Feed ]]>
                </title>
                <description>
                    <![CDATA[ News Feed ]]>
                </description>
                <link>https://www.ft.com/news-feed</link>
                <generator>RSS for Node</generator>
                <lastBuildDate>Sun, 12 Mar 2023 13:26:24 GMT</lastBuildDate>
                <atom:link href="https://www.ft.com/news-feed?format=rss" rel="self" type="application/rss+xml"/>
                <copyright>
                    <![CDATA[ © Copyright The Financial Times Ltd 2023. "FT" and "Financial Times" are trademarks of the Financial Times. See http://www.ft.com/servicestools/help/terms#legal1 for the terms and conditions of reuse. ]]>
                </copyright>
                <language>
                    <![CDATA[ en ]]>
                </language>
                <webMaster>
                    <![CDATA[ client.support@ft.com (FT Client Support) ]]>
                </webMaster>
                <ttl>15</ttl>
                <category>
                    <![CDATA[ Newspapers ]]>
                </category>
                <item>
                    <title>
                        <![CDATA[ Three global cities are pulling ahead since the peak of the pandemic ]]>
                    </title>
                    <description>
                        <![CDATA[ Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs ]]>
                    </description>
                    <link>https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6</link>
                    <guid isPermaLink="false">1cf1b55e-bb8d-435a-95a3-5d21149939b6</guid>
                    <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
                </item>
                <item>
                    <title>
                        <![CDATA[ UK seeks to tap Middle East money to buy out SVB unit ]]>
                    </title>
                    <description>
                        <![CDATA[ ‘Lead white knight’ eyeing British arm of tech lender that had billions in deposits ]]>
                    </description>
                    <link>https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae</link>
                    <guid isPermaLink="false">cde4aa95-1cb5-408d-b35f-3216eaee46ae</guid>
                    <pubDate>Sun, 12 Mar 2023 12:54:53 GMT</pubDate>
                </item>
            </channel>
        </rss>
    """
    expected = [
        {
            "description": "Miami, Dubai and Singapore boom by welcoming those chased "
            "out of rival international hubs",
            "published": "Sun, 12 Mar 2023 13:00:35 GMT",
            "title": "Three global cities are pulling ahead since the peak of the "
            "pandemic",
            "url": "https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            "source_url": "https://www.ft.com/news-feed",
        },
        {
            "description": "‘Lead white knight’ eyeing British arm of tech lender that "
            "had billions in deposits",
            "published": "Sun, 12 Mar 2023 12:54:53 GMT",
            "title": "UK seeks to tap Middle East money to buy out SVB unit",
            "url": "https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            "source_url": "https://www.ft.com/news-feed",
        },
    ]

    actual = http_client.parse_xml(xml)

    assert actual == expected


@responses.activate
def test_http_client_when_content_type_is_text():
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://www.ft.com/",
            "body": "Hello World",
            "status": 200,
            "content_type": "text/html",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.GET,
        url="https://www.ft.com/",
        headers={"Content-Type": "text/html"},
        params=None,
    )

    assert actual == "Hello World"


@responses.activate
def test_http_client_when_content_type_is_zip():
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://www.ft.com/",
            "body": "Hello World",
            "status": 200,
            "content_type": "application/zip",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.GET,
        url="https://www.ft.com/",
        headers={"Content-Type": "application/zip"},
        params=None,
    )

    assert actual == b"Hello World"
