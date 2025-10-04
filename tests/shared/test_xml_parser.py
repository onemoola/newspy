from unittest.mock import Mock
from newspy.shared import xml_parser


def test_parse_xml():
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
                        <![CDATA[ 'Lead white knight' eyeing British arm of tech lender that had billions in deposits ]]>
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
            "description": "'Lead white knight' eyeing British arm of tech lender that "
            "had billions in deposits",
            "published": "Sun, 12 Mar 2023 12:54:53 GMT",
            "title": "UK seeks to tap Middle East money to buy out SVB unit",
            "url": "https://www.ft.com/content/cde4aa95-1cb5-408d-b35f-3216eaee46ae",
            "source_url": "https://www.ft.com/news-feed",
        },
    ]

    actual = xml_parser.parse_xml(data=xml, source_url="https://www.ft.com/news-feed")

    assert actual == expected


def test_parse_xml_with_missing_title():
    xml = """
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
            <channel>
                <item>
                    <description>
                        <![CDATA[ This item has no title ]]>
                    </description>
                    <link>https://example.com/article</link>
                    <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
                </item>
            </channel>
        </rss>
    """

    actual = xml_parser.parse_xml(data=xml, source_url="https://example.com/feed")

    assert actual is None


def test_parse_xml_with_no_items():
    xml = """
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
            <channel>
                <title>
                    <![CDATA[ News Feed ]]>
                </title>
            </channel>
        </rss>
    """

    actual = xml_parser.parse_xml(data=xml, source_url="https://example.com/feed")

    assert actual is None


def test_parse_xml_with_atom_feed():
    xml = """
        <feed xmlns="http://www.w3.org/2005/Atom">
            <title>Example Feed</title>
            <entry>
                <title>Atom Test Article</title>
                <summary>This is a test summary</summary>
                <link href="https://example.com/atom-article"/>
                <published>2023-03-12T13:00:35Z</published>
            </entry>
        </feed>
    """

    actual = xml_parser.parse_xml(data=xml, source_url="https://example.com/atom-feed")

    assert actual is not None
    assert len(actual) == 1
    assert actual[0]["title"] == "Atom Test Article"
    assert actual[0]["description"] == "This is a test summary"
    assert actual[0]["url"] == "https://example.com/atom-article"


def test_parse_xml_with_content_encoded():
    xml = """
        <rss xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <content:encoded><![CDATA[ Rich content here ]]></content:encoded>
                    <link>https://example.com/article</link>
                    <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
                </item>
            </channel>
        </rss>
    """

    actual = xml_parser.parse_xml(data=xml, source_url="https://example.com/feed")

    assert actual is not None
    assert len(actual) == 1
    assert actual[0]["title"] == "Test Article"
    assert actual[0]["description"] == "Rich content here"


def test_parse_xml_with_long_text():
    xml = """
        <rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
            <channel>
                <title>
                    <![CDATA[ News Feed ]]>
                </title>
                <item>
                    <title>
                        <![CDATA[ A Very Long Title That Exceeds Typical Length Limits and Should Be Truncated Appropriately ]]>
                    </title>
                    <description>
                        <![CDATA[ This is a test description that also happens to be excessively long and should be truncated when parsed by the XML parser to ensure that it does not break anything in the process. ]]>
                    </description>
                    <link>https://example.com/article-with-long-text</link>
                    <pubDate>Sun, 12 Mar 2023 13:00:35 GMT</pubDate>
                </item>
            </channel>
        </rss>
    """

    actual = xml_parser.parse_xml(data=xml, source_url="https://example.com/feed")

    assert actual is not None
    assert len(actual) == 1
    assert (
        actual[0]["title"]
        == "A Very Long Title That Exceeds Typical Length Limits and Should Be Truncated Appropriately"
    )
    assert (
        actual[0]["description"]
        == "This is a test description that also happens to be excessively long and should be truncated when parsed by the XML parser to ensure that it does not break anything in the process."
    )


def test_get_text_content_with_attribute_error():
    item = Mock()
    item.find.side_effect = [AttributeError("Mock error"), Mock(text="Test Article")]

    result = xml_parser._get_text_content(item, ["nonexistent", "title"], {})

    assert result == "Test Article"


def test_get_text_content_with_key_error():
    item = Mock()
    title_elem = Mock()
    title_elem.text = "Test Article"
    item.find.side_effect = [KeyError("Mock error"), title_elem]

    result = xml_parser._get_text_content(item, ["nonexistent", "title"], {})

    assert result == "Test Article"


def test_get_link_with_attribute_error():
    item = Mock()
    item.find.side_effect = [
        None,
        AttributeError("Mock error"),
        AttributeError("Mock error"),
    ]

    result = xml_parser._get_link(item, {"atom": "http://www.w3.org/2005/Atom"})

    assert result == ""


def test_get_link_with_key_error():
    item = Mock()
    item.find.side_effect = [None, KeyError("Mock error"), KeyError("Mock error")]

    result = xml_parser._get_link(item, {"atom": "http://www.w3.org/2005/Atom"})

    assert result == ""
