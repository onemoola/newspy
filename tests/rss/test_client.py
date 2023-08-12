from pathlib import Path

import responses

from newspy import rss
from newspy.rss.client import URL
from newspy.rss.models import RssSource, RssCategory, RssArticle
from newspy.shared.models import Language


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
            title="Three global cities are pulling ahead since the peak of the pandemic",
            description="Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs",
            url="https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            published="Sun, 12 Mar 2023 13:00:35 GMT",
        ),
        RssArticle(
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
            category=RssCategory.FINANCIAL,
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
            category=RssCategory.FINANCIAL,
            language=Language.EN,
        )
    ]

    actual = rss.get_articles(sources=rss_sources)

    assert actual == []


def test_get_rss_sources_from_local_path() -> None:
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=RssCategory.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=RssCategory.BUSINESS,
            language=Language.EN,
        ),
    ]
    actual = rss.get_sources(file_path=Path("tests/data/rss_sources.csv.gz"))

    assert actual == expected


@responses.activate
def test_get_rss_resources_from_remote_path():
    expected = [
        RssSource(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            description="The Wall Street Journal (WSJ) Markets RSS",
            url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            category=RssCategory.FINANCIAL,
            language=Language.EN,
        ),
        RssSource(
            id="wsj-business",
            name="The Wall Street Journal Business",
            description="The Wall Street Journal (WSJ) Business RSS",
            url="https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            category=RssCategory.BUSINESS,
            language=Language.EN,
        ),
    ]

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://github.com/onemoola/newspy/tree/main/data/rss_sources.csv.gz",
            "body": "tests/data/rss_sources.csv.gz",
            "status": 200,
            "content_type": "application/zip",
        }
    )

    actual = rss.get_sources(
        file_path=URL(
            "https://github.com/onemoola/newspy/tree/main/data/rss_sources.csv.gz"
        )
    )

    assert actual == expected


def test_get_rss_resources_from_invalid_path():
    actual = rss.get_sources(file_path=123)  # type: ignore

    assert actual == []
