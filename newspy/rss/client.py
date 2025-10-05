import csv
import gzip
import logging
import io
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import NewType

from newspy.models import Category
from newspy.rss.models import RssSource, RssArticle
from newspy.shared.http_client import HttpClient, HttpMethod
from newspy.shared.exceptions import NewspyException

DEFAULT_USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
)
URL = NewType("URL", str)

logger = logging.getLogger(__name__)


def get_articles(
    category: Category | None = None,
    language: str | None = None,
    sources: list[RssSource] | None = None,
    **kwargs,
) -> list[RssArticle]:
    if not sources:
        sources = get_sources(category=category, language=language)

    http_client = HttpClient()

    articles = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                http_client.send,
                method=HttpMethod.GET,
                url=source.url,
                headers={"User-Agent": DEFAULT_USER_AGENT},
                params=None,
                payload=None,
            )
            for source in sources
        ]

        for future in as_completed(futures):
            try:
                resp_json = future.result()
            except NewspyException as exc:
                logger.warning("Skipping a source due to error: %s", exc)
                continue

            if resp_json and isinstance(resp_json, list):
                for article in resp_json:
                    source = filter(lambda s: s.url == article["source_url"], sources)
                    articles.append(
                        RssArticle(
                            source=next(source),
                            title=article["title"],
                            description=article["description"],
                            url=article["url"],
                            published=article["published"],
                        )
                    )

    return articles


def get_sources(
    category: Category | None = None,
    language: str | None = None,
    file_path: Path | URL = URL(
        "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true"
    ),
    **kwargs,
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
        if category and language:
            sources = [
                RssSource(**row)
                for row in reader
                if row["category"] == category and row["language"] == language
            ]
        elif category:
            sources = [
                RssSource(**row) for row in reader if row["category"] == category
            ]
        elif language:
            sources = [
                RssSource(**row) for row in reader if row["language"] == language
            ]
        else:
            sources = [RssSource(**row) for row in reader]

    return sources
