from xml.etree import ElementTree


def parse_xml(data: str, source_url: str) -> list[dict[str, str]] | None:
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError:
        return None

    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "content": "http://purl.org/rss/1.0/modules/content/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "media": "http://search.yahoo.com/mrss/",
    }

    items = []

    rss_items = root.findall(".//item")

    if not rss_items:
        rss_items = root.findall(".//atom:entry", namespaces) or root.findall(
            ".//{http://www.w3.org/2005/Atom}entry"
        )

    for item in rss_items:
        parsed_item = _parse_feed_item(item, source_url, namespaces)
        if parsed_item:
            items.append(parsed_item)

    return items if items else None


def _parse_feed_item(
    item: ElementTree.Element, source_url: str, namespaces: dict
) -> dict[str, str] | None:
    title = _get_text_content(
        item,
        [
            "title",
            "atom:title",
            "{http://www.w3.org/2005/Atom}title",
        ],
        namespaces,
    )

    description = _get_text_content(
        item,
        [
            "description",
            "content:encoded",
            "atom:summary",
            "{http://www.w3.org/2005/Atom}summary",
            "atom:content",
            "{http://www.w3.org/2005/Atom}content",
            "summary",
        ],
        namespaces,
    )

    link = _get_link(item, namespaces)

    pub_date = _get_text_content(
        item,
        [
            "pubDate",
            "published",
            "atom:published",
            "{http://www.w3.org/2005/Atom}published",
            "atom:updated",
            "{http://www.w3.org/2005/Atom}updated",
            "dc:date",
            "date",
        ],
        namespaces,
    )

    if not title:
        return None

    return {
        "source_url": source_url,
        "title": title or "",
        "description": description or "",
        "url": link or "",
        "published": pub_date or "",
    }


def _get_text_content(
    element: ElementTree.Element, paths: list[str], namespaces: dict
) -> str:
    for path in paths:
        try:
            if ":" in path and not path.startswith("{"):
                found = element.find(path, namespaces)
            else:
                found = element.find(path)

            if found is not None:
                text = found.text
                if text:
                    return text.strip()
        except (AttributeError, KeyError):
            continue

    return ""


def _get_link(element: ElementTree.Element, namespaces: dict) -> str:
    link = _get_text_content(element, ["link"], namespaces)
    if link:
        return link

    for link_path in ["atom:link", "{http://www.w3.org/2005/Atom}link"]:
        try:
            link_elem = element.find(link_path, namespaces)
            if link_elem is not None and "href" in link_elem.attrib:
                return link_elem.attrib["href"].strip()
        except (AttributeError, KeyError):
            continue

    return ""
