from pathlib import Path

import responses

from newspy import rss
from newspy.models import Language, Category
from newspy.rss.client import URL
from newspy.rss.models import RssSource, RssArticle


@responses.activate
def test_get_rss_articles(rss_articles_res_xml) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "body": rss_articles_res_xml,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    expected = [
        RssArticle(
            source=RssSource(
                id="wsj-markets",
                name="The Wall Street Journal Markets",
                description="The Wall Street Journal (WSJ) Markets RSS",
                url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                category=Category.FINANCIAL,
                language=Language.EN,
            ),
            title="Three global cities are pulling ahead since the peak of the pandemic",
            description="Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs",
            url="https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            published="Sun, 12 Mar 2023 13:00:35 GMT",
        ),
        RssArticle(
            source=RssSource(
                id="wsj-markets",
                name="The Wall Street Journal Markets",
                description="The Wall Street Journal (WSJ) Markets RSS",
                url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                category=Category.FINANCIAL,
                language=Language.EN,
            ),
            title="UK seeks to tap Middle East money to buy out SVB unit",
            description="‘Lead white knight’ eyeing British arm of tech lender that had billions in deposits",
            url="https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            published="Sun, 12 Mar 2023 12:54:53 GMT",
        ),
    ]
    rss_sources = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        )
    ]
    actual = rss.get_articles(sources=rss_sources)

    assert actual == expected


@responses.activate
def test_get_rss_articles_return_none(rss_articles_res_broken_xml) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "body": rss_articles_res_broken_xml,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    rss_sources = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        )
    ]

    actual = rss.get_articles(sources=rss_sources)

    assert actual == []


@responses.activate
def test_get_rss_articles_handles_string_response() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "body": "<html><body>404 Not Found</body></html>",
            "status": 200,
            "content_type": "text/html",
        }
    )

    rss_sources = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        )
    ]

    actual = rss.get_articles(sources=rss_sources)

    assert actual == []


@responses.activate
def test_get_rss_articles_handles_none_response() -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "body": "",
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    rss_sources = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        )
    ]

    actual = rss.get_articles(sources=rss_sources)

    assert actual == []


@responses.activate
def test_get_rss_articles_handles_http_exception(rss_articles_res_xml) -> None:
    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "json": {
                "error": {"message": "Service unavailable", "reason": "server_error"}
            },
            "status": 503,
            "content_type": "application/json",
        }
    )

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            "body": rss_articles_res_xml,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    rss_sources = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=Category.BUSINESS,
            language=Language.EN,
        ),
    ]

    actual = rss.get_articles(sources=rss_sources)

    assert len(actual) == 2
    assert all(article.source.id == "wsj-business" for article in actual)
    assert (
        actual[0].title
        == "Three global cities are pulling ahead since the peak of the pandemic"
    )
    assert actual[1].title == "UK seeks to tap Middle East money to buy out SVB unit"


def test_get_rss_sources_from_local_path() -> None:
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=Category.BUSINESS,
            language=Language.EN,
        ),
    ]
    actual = rss.get_sources(file_path=Path("tests/data/rss_sources.csv.gz"))

    assert actual == expected


def test_get_rss_sources_from_invalid_path() -> None:
    actual = rss.get_sources(file_path=123)  # type: ignore

    assert actual == []


def test_get_rss_sources_with_category() -> None:
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        )
    ]
    actual = rss.get_sources(
        file_path=Path("tests/data/rss_sources.csv.gz"), category=Category.FINANCIAL
    )

    assert actual == expected


def test_get_rss_sources_with_language() -> None:
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=Category.BUSINESS,
            language=Language.EN,
        ),
    ]
    actual = rss.get_sources(
        file_path=Path("tests/data/rss_sources.csv.gz"), language=Language.EN
    )

    assert actual == expected


def test_get_rss_sources_with_category_and_language() -> None:
    expected = [
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=Category.BUSINESS,
            language=Language.EN,
        ),
    ]
    actual = rss.get_sources(
        file_path=Path("tests/data/rss_sources.csv.gz"),
        category=Category.BUSINESS,
        language=Language.EN,
    )

    assert actual == expected


@responses.activate
def test_get_rss_resources_from_remote_path():
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=Category.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=Category.BUSINESS,
            language=Language.EN,
        ),
    ]

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true",
            "body": open("tests/data/rss_sources.csv.gz", "rb").read(),
            "status": 200,
            "content_type": "application/zip",
        }
    )

    actual = rss.get_sources(
        file_path=URL(
            "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true"
        )
    )

    assert actual == expected


def test_get_rss_resources_from_invalid_path():
    actual = rss.get_sources(file_path=123)  # type: ignore

    assert actual == []
