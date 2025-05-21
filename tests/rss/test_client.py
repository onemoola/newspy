import pytest
import asyncio
import gzip
import io
from pathlib import Path
from unittest.mock import AsyncMock, patch

from newspy import rss
from newspy.models import Language, Category
from newspy.rss.client import URL # Assuming this is still used or can be adapted
from newspy.rss.models import RssSource, RssArticle
from newspy.shared.http_client import HttpClient # For mocking

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

# Sample RSS XML for mocking article fetching
SAMPLE_RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Sample RSS Feed</title>
    <link>http://example.com/</link>
    <description>A sample RSS feed for testing.</description>
    <item>
        <title>Article 1 Title</title>
        <link>http://example.com/article1</link>
        <description>Description for article 1.</description>
        <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
    </item>
    <item>
        <title>Article 2 Title</title>
        <link>http://example.com/article2</link>
        <description>Description for article 2.</description>
        <pubDate>Sun, 12 Mar 2023 12:54:53 GMT</pubDate>
    </item>
</channel>
</rss>
"""

# Sample broken RSS XML
SAMPLE_BROKEN_RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Sample RSS Feed</title>
    <item>
        <title>Article 1 Title</title>
        <link>http://example.com/article1</link>
        <description>Description for article 1.</description>
    </item> <!-- Missing pubDate, and other issues could be introduced -->
</rss>
"""

# Sample CSV content for rss_sources.csv.gz
SAMPLE_SOURCES_CSV_CONTENT = """id,name,description,url,category,language
wsj-markets,The Wall Street Journal Markets,The Wall Street Journal (WSJ) Markets RSS,https://feeds.a.dj.com/rss/RSSMarketsMain.xml,financial,en
wsj-business,The Wall Street Journal Business,The Wall Street Journal (WSJ) Business RSS,https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml,business,en
"""

@pytest.fixture
def mock_http_client_send():
    # This fixture provides a mock for the HttpClient.send method directly
    # This is useful if the HttpClient instance is created inside the functions being tested
    # and not passed in as an argument.
    # If HttpClient is passed as an argument, then an AsyncMock(spec=HttpClient) is better.
    # Given the refactored clients, passing a mocked HttpClient is the way.
    mock_client = AsyncMock(spec=HttpClient)
    return mock_client


async def test_get_rss_articles_async(mock_http_client_send, rss_articles_res_xml):
    # rss_articles_res_xml fixture seems to be from conftest.py providing XML string
    # In an async world, parse_xml in http_client expects bytes
    # For this test, we assume parse_xml inside http_client.send is what we want to mock the output of
    # So, mock_http_client_send.send should return the *parsed* structure from parse_xml
    
    # The actual send method returns a list of dicts after parsing XML
    parsed_xml_output = [
        {
            "source_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", # This should match the source's URL
            "title": "Three global cities are pulling ahead since the peak of the pandemic",
            "description": "Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs",
            "url": "https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            "published": "Sun, 12 Mar 2023 13:00:35 GMT",
        },
        {
            "source_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "title": "UK seeks to tap Middle East money to buy out SVB unit",
            "description": "‘Lead white knight’ eyeing British arm of tech lender that had billions in deposits",
            "url": "https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            "published": "Sun, 12 Mar 2023 12:54:53 GMT",
        },
    ]
    mock_http_client_send.send.return_value = parsed_xml_output

    rss_source_instance = RssSource(
        id="wsj-markets",
        name="The Wall Street Journal Markets",
        description="The Wall Street Journal (WSJ) Markets RSS",
        url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml", # This URL is used by send
        category=Category.FINANCIAL,
        language=Language.EN,
    )
    
    expected = [
        RssArticle(
            source=rss_source_instance,
            title="Three global cities are pulling ahead since the peak of the pandemic",
            description="Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs",
            url="https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            published="Sun, 12 Mar 2023 13:00:35 GMT",
            archived_data=None,
        ),
        RssArticle(
            source=rss_source_instance,
            title="UK seeks to tap Middle East money to buy out SVB unit",
            description="‘Lead white knight’ eyeing British arm of tech lender that had billions in deposits",
            url="https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            published="Sun, 12 Mar 2023 12:54:53 GMT",
            archived_data=None,
        ),
    ]

    actual = await rss.get_articles(sources=[rss_source_instance], http_client=mock_http_client_send)
    
    mock_http_client_send.send.assert_called_once_with(
        method=rss.HttpMethod.GET,
        url="https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        headers={"Content-Type": rss.ContentType.XML},
    )
    assert actual == expected

async def test_get_rss_articles_return_empty_on_error(mock_http_client_send):
    mock_http_client_send.send.return_value = None # Simulate error or no data from parsing
    
    rss_source_instance = RssSource(
        id="wsj-markets", name="Test", description="Test", 
        url="http://example.com/feed.xml", category=Category.GENERAL, language=Language.EN
    )
    actual = await rss.get_articles(sources=[rss_source_instance], http_client=mock_http_client_send)
    assert actual == []

async def test_get_rss_sources_from_local_path_async() -> None:
    # This test remains largely synchronous in its setup, but the function it calls is async
    # if it were to use an http_client for local files (which it doesn't for Path objects).
    # The current get_sources handles Path objects synchronously for file reading.
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
