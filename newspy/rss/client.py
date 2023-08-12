import csv
import gzip
import io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import NewType

from newspy.rss.models import RssSource, RssArticle
from newspy.shared.http_client import HttpClient, HttpMethod

URL = NewType("URL", str)


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

            if resp_json:
                for article in resp_json:
                    articles.append(RssArticle(**article))

    return articles


def get_sources(
    file_path: (Path | URL) = URL(
        "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true"
    ),
) -> list[RssSource]:
    if isinstance(file_path, Path):
        file_content = file_path
    elif isinstance(file_path, str):
        http_client = HttpClient()
        file_content = http_client.send(
            method=HttpMethod.GET,
            url=file_path,
            headers={"Content-Type": "application/zip"},
        )
        file_content = io.BytesIO(file_content)
    else:
        return []

    with gzip.open(file_content, "rt") as f:
        reader = csv.DictReader(f)
        sources = [RssSource(**row) for row in reader]

    return sources
