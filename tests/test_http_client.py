import json

import pytest
import responses

from newspy.exceptions import NewspyException
from newspy.http_client import HttpClient, HttpMethod
from newspy.models import ArticlesRes

API_KEY = "seckfkdLkkekeKy"

BASE_URL = "https://localhost/v2/top-headlines"
HEADERS = {
    "content_type": "application/json",
}
PARAMS = {
    "apiKey": API_KEY,
    "sources": "bloomberg,business-insider",
    "language": "en",
    "pageSize": 100,
}


@responses.activate
def test_http_client(article_res_json) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": article_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    http_client = HttpClient()
    actual = http_client.send(
        method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
    )

    article_res = ArticlesRes.parse_obj(actual)
    assert article_res.status == "ok"
    assert article_res.totalResults == 86
    assert len(article_res.articles) == 1


@responses.activate
def test_http_client_when_http_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps(
                {
                    "error": {
                        "message": "Bad request"
                    }
                }
            ),
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyException):
        http_client = HttpClient()
        http_client.send(
            method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
        )


@responses.activate
def test_http_client_when_http_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps(
                {
                    "error": {
                        "message": "Bad request"
                    }
                }
            ),
            "status": 404,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyException):
        http_client = HttpClient()
        http_client.send(
            method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
        )


@responses.activate
def test_http_client_when_server_error() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": f"{BASE_URL}?apiKey={API_KEY}&sources=bloomberg,business-insider&language=en&pageSize=100",
            "body": json.dumps(
                {
                    "error": {
                        "message": "Bad request"
                    }
                }
            ),
            "status": 500,
            "content_type": "application/json",
        }
    )

    with pytest.raises(NewspyException):
        http_client = HttpClient()
        http_client.send(
            method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
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

    http_client = HttpClient()
    actual = http_client.send(
        method=HttpMethod.GET, url=BASE_URL, headers=HEADERS, params=PARAMS
    )

    assert actual is None
    