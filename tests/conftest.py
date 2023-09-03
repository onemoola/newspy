import json

import pytest

from newspy.newsorg.models import (
    NewsorgArticle,
    NewsorgArticlesRes,
    NewsorgSource,
)


@pytest.fixture
def newsorg_source() -> NewsorgSource:
    return NewsorgSource(id="fortune", name="Fortune")


@pytest.fixture
def newsorg_article(newsorg_source) -> NewsorgArticle:
    return NewsorgArticle(
        source=newsorg_source,
        author="Emma Hinchliffe, Paige McGlauflin",
        title="Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
        description="Former SoftBank partner and Facebook India director Kirthiga Reddy is the cofounder of Laddrr, "
        "a resource hub for working mothers aiming to prevent mid-career drop-off.",
        url="https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for-working-mothers/",
        urlToImage="https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
        publishedAt="2022-06-01T13:22:34Z",
        content="Skip to Content",
    )


@pytest.fixture
def newsorg_articles_res(newsorg_article) -> NewsorgArticlesRes:
    return NewsorgArticlesRes(status="ok", totalResults=86, articles=[newsorg_article])


@pytest.fixture
def newsorg_articles_res_json() -> json:
    return json.dumps(
        {
            "status": "ok",
            "totalResults": 86,
            "articles": [
                {
                    "source": {"id": "fortune", "name": "Fortune"},
                    "author": "Emma Hinchliffe, Paige McGlauflin",
                    "title": "Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
                    "description": "Former SoftBank partner and Facebook India director Kirthiga Reddy is the "
                    "cofounder of Laddrr, a resource hub for working mothers aiming to prevent "
                    "mid-career drop-off.",
                    "url": "https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for"
                    "-working-mothers/",
                    "urlToImage": "https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
                    "publishedAt": "2022-06-01T13:22:34Z",
                    "content": "Skip to Content",
                }
            ],
        }
    )


@pytest.fixture
def newsorg_articles_res_broken_json() -> json:
    return json.dumps(
        {
            "status": 0000,
            "totalResults": "86",
            "articles": [
                {
                    "source": {"id": "fortune", "name": "Fortune"},
                    "author": "Emma Hinchliffe, Paige McGlauflin",
                    "long_title": "Why a former SoftBank partner is tackling mid-career drop-off for working mothers",
                    "description": "Former SoftBank partner and Facebook India director Kirthiga Reddy is the "
                    "cofounder of Laddrr, a resource hub for working mothers aiming to prevent "
                    "mid-career drop-off.",
                    "url": "https://fortune.com/2022/06/01/former-softbank-partner-tackling-mid-career-drop-off-for"
                    "-working-mothers/",
                    "urlToImage": "https://content.fortune.com/wp-content/uploads/2022/05/Kirthiga1.jpg?resize=1200,600",
                    "publishedAt": "2022-06-01T13:22:34Z",
                    "content": "Skip to Content",
                }
            ],
        }
    )


@pytest.fixture
def newsorg_sources_res_json() -> json:
    return json.dumps(
        {
            "status": "ok",
            "sources": [
                {
                    "id": "abc-news",
                    "name": "ABC News",
                    "description": "Your trusted source for breaking news, analysis, exclusive interviews, headlines, "
                    "and videos at ABCNews.com.",
                    "url": "https://abcnews.go.com",
                    "category": "general",
                    "language": "en",
                    "country": "us",
                }
            ],
        }
    )


@pytest.fixture
def newsorg_sources_res_broken_json() -> json:
    return json.dumps(
        {
            "status": 2,
            "sources": [
                {
                    "id": "abc-news",
                    "full_name": "ABC News",
                    "description": "Your trusted source for breaking news, analysis, exclusive interviews, headlines, "
                    "and videos at ABCNews.com.",
                    "url": "https://abcnews.go.com",
                    "category": "general",
                    "language": "en",
                    "country": "us",
                }
            ],
        }
    )


@pytest.fixture
def rss_articles_res_xml() -> str:
    return """
            <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
                <channel>
                    <title>
                        <![CDATA[ News Feed ]]>
                    </title>
                    <description>
                        <![CDATA[ News Feed ]]>
                    </description>
                    <link>https://feeds.a.dj.com/rss/RSSMarketsMain.xml</link>
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


@pytest.fixture
def rss_articles_res_broken_xml() -> str:
    return """
            <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
                <channel>
                    <long_title>
                        <![CDATA[ News Feed ]]>
                    </long_title>
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
                        <description>
                            <![CDATA[ Miami, Dubai and Singapore boom by welcoming those chased out of rival international hubs ]]>
                        </description>
                        <link>https://www.ft.com/content/1cf1b55e-bb8d-435a-95a3-5d21149939b6</link>
                        <guid isPermaLink="false">1cf1b55e-bb8d-435a-95a3-5d21149939b6</guid>
                        <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
                    </item>
                    <item>
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
