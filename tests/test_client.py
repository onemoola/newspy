from datetime import datetime, timezone

import responses

import newspy.client as newspy
from newspy.shared.models import Source, Channel, Article, Language, Category

API_KEY = "seckfkdLkkekeKy"


def test_configure_without_newsorg_api_key() -> None:
    newspy.configure()
    actual = newspy.default_client_config.get("newsorg_api_key")

    assert actual is None


def test_configure_with_newsorg_api_key() -> None:
    newspy.configure(newsorg_api_key="test")
    actual = newspy.default_client_config.get("newsorg_api_key")

    assert actual == "test"


@responses.activate
def test_get_sources(newsorg_sources_res_json) -> None:
    expected = [
        Source(
            id="abc-news",
            name="ABC News",
            channel=Channel.NEWSORG,
        ),
        Source(
            id="wsj-markets",
            name="The Wall Street Journal Markets",
            channel=Channel.RSS,
        ),
        Source(
            id="wsj-business",
            name="The Wall Street Journal Business",
            channel=Channel.RSS,
        ),
    ]
    responses.add(
        **{
            "method": responses.GET,
            "url": f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}",
            "body": newsorg_sources_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true",
            "body": open("tests/data/rss_sources.csv.gz", "rb").read(),
            "status": 200,
            "content_type": "application/zip",
        }
    )

    newspy.configure(newsorg_api_key=API_KEY)
    actual = newspy.get_sources()

    assert actual.sort(key=lambda x: x.id) == expected.sort(key=lambda x: x.id)


@responses.activate
def test_get_articles(newsorg_articles_res_json, rss_articles_res_xml) -> None:
    expected = [
        Article(
            slug="fortune-why-a-former-softbank-partner-is-tackling-midcareer-dropoff-for-working-mothers",
            url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
            url_to_image="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
            title="Why a former SoftBank partner is tackling mid-career drop-off "
            "for working mothers",
            abstract="Former SoftBank partner and Facebook India director "
            "Kirthiga Reddy is the cofounder of Laddrr, a resource hub "
            "for working mothers aiming to prevent mid-career drop-off.",
            author="Emma Hinchliffe, Paige McGlauflin",
            source=Source(id="fortune", name="Fortune", channel=Channel.NEWSORG),
            published=datetime(2022, 6, 1, 13, 22, 34, tzinfo=timezone.utc),
        ),
        Article(
            slug="the-wall-street-journal-markets-three-global-cities-are-pulling-ahead-since-the-peak-of-the-pandemic",
            url="https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6",
            url_to_image=None,
            title="Three global cities are pulling ahead since the peak of the "
            "pandemic",
            abstract="Miami, Dubai and Singapore boom by welcoming those chased "
            "out of rival international hubs",
            author=None,
            source=Source(
                id="wsj-markets",
                name="The Wall Street Journal Markets",
                channel=Channel.RSS,
            ),
            published=datetime(2023, 3, 12, 13, 0, 35),
        ),
        Article(
            slug="the-wall-street-journal-markets-uk-seeks-to-tap-middle-east-money-to-buy-out-svb-unit",
            url="https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            url_to_image=None,
            title="UK seeks to tap Middle East money to buy out SVB unit",
            abstract="‘Lead white knight’ eyeing British arm of tech lender that "
            "had billions in deposits",
            author=None,
            source=Source(
                id="wsj-markets",
                name="The Wall Street Journal Markets",
                channel=Channel.RSS,
            ),
            published=datetime(2023, 3, 12, 12, 54, 53),
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

    responses.add(
        **{
            "method": responses.GET,
            "url": f"https://newsapi.org/v2/top-headlines?apiKey={API_KEY}&language=en&pageSize=100&page=1",
            "body": newsorg_articles_res_json,
            "status": 200,
            "content_type": "application/json",
        }
    )

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "body": rss_articles_res_xml,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    responses.add(
        **{
            "method": responses.GET,
            "url": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            "body": None,
            "status": 200,
            "content_type": "application/rss+xml",
        }
    )

    newspy.configure(newsorg_api_key=API_KEY)
    actual = newspy.get_articles(language=Language.EN)

    assert actual == expected


def test_categories() -> None:
    expected = [
        Category.BUSINESS,
        Category.FINANCIAL,
        Category.ENTERTAINMENT,
        Category.GENERAL,
        Category.HEALTH,
        Category.SCIENCE,
        Category.SPORTS,
        Category.TECHNOLOGY,
    ]

    actual = newspy.get_categories()

    assert actual == expected
