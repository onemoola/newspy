import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from newspy.rss.models import RssSource, RssArticle
from newspy.shared.exceptions import NewspyException
from newspy.shared.http_client import HttpClient, HttpMethod


def get_articles(sources: list[RssSource] | None = None) -> list[RssArticle]:
    if not sources:
        sources = get_sources()

    http_client = HttpClient()

    articles = []
    with ThreadPoolExecutor() as executor:
        for source in sources:
            future = executor.submit(
                http_client.send,
                method=HttpMethod.GET,
                url=source.url,
                headers={"Content-Type": "application/rss+xml"},
                params=None,
                payload=None,
            )

            resp_json = future.result()

            try:
                if resp_json:
                    for article in resp_json:
                        articles.append(RssArticle(**article))
            except TypeError as err:
                raise NewspyException(
                    msg=f"Failed to validate the RSS articles response json: {resp_json}",
                    reason=str(err),
                )

    return articles


def get_sources() -> list[RssSource]:
    with open(Path("newspy/data/rss_sources.csv"), "r") as f:
        reader = csv.DictReader(f)
        sources = [RssSource(**row) for row in reader]

    return sources
