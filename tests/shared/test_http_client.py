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
def test_http_client_when_requests_session_is_false(newsorg_articles_res_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": newsorg_articles_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    client = HttpClient(requests_session=False)
    actual = client.send(
        method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
    )

    assert actual is not None


@responses.activate
def test_http_client_with_payload(newsorg_articles_res_json) -> None:
    responses.add(
        **{
            "method": responses.POST,
            "url": BASE_URL,
            "body": newsorg_articles_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.POST, url=BASE_URL, headers=HEADERS, payload={"data": "data"}
    )

    assert actual is not None


@responses.activate
def test_http_client_when_payload_is_string() -> None:
    responses.add(
        **{
            "method": responses.POST,
            "url": BASE_URL,
            "body": "Hello World",
            "status": 200,
            "content_type": "application/json",
        }
    )

    client = HttpClient()
    actual = client.send(
        method=HttpMethod.POST,
        url=BASE_URL,
        headers={
            "Content-Type": "application/text",
        },
        payload="data",
    )

    assert actual == "Hello World"


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

    with pytest.raises(NewspyHttpException, match="status code: 404"):
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)


@responses.activate
def test_http_client_when_http_error_is_text() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": "Bad request",
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyHttpException) as exc:
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)

    assert (
        str(exc.value)
        == "status code: 404, message: https://localhost/v2/top-headlines?apiKey=seckfkdLkkekeKy&sources=bloomberg"
        "%2Cbusiness-insider&language=en&pageSize=100:\n Bad request, reason: None"
    )


@responses.activate
def test_http_client_when_http_error_with_json() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps({"error": {"message": "Bad request"}}),
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyHttpException, match="status code: 404"):
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

    with pytest.raises(NewspyHttpException) as ex:
        client = HttpClient()
        client.send(method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS)

    assert str(ex.value) == (
        "status code: 429, message: https://localhost/v2/top-headlines?apiKey=seckfkdLkkekeKy&sources=bloomberg"
        "%2Cbusiness-insider&language=en&pageSize=100:\n Max Retries, reason: too many 500 error "
        "responses"
    )


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
            "source_url": "https://www.ft.com/",
        },
        {
            "description": "‘Lead white knight’ eyeing British arm of tech lender that "
            "had billions in deposits",
            "published": "Sun, 12 Mar 2023 12:54:53 GMT",
            "title": "UK seeks to tap Middle East money to buy out SVB unit",
            "url": "https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            "source_url": "https://www.ft.com/",
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
