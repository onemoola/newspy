import os
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from newspy import newsorg, rss
from newspy.models import Article, Category, Channel, Country, Language, Source

default_client_config = {}

channels = {
    Channel.NEWSORG: newsorg,
    Channel.RSS: rss,
}


def run_async_task(awaitable):
    """Helper function to run an awaitable in a new event loop."""
    return asyncio.run(awaitable)


def configure(newsorg_api_key: str | None = None) -> None:
    global default_client_config

    if newsorg_api_key is None:
        newsorg_api_key = os.getenv("NEWSORG_API_KEY")

    default_client_config = {
        "newsorg_api_key": newsorg_api_key,
    }


def get_sources(
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
) -> list[Source]:
    sources = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for key in channels:
            client_module = channels[key].client
            if key == Channel.RSS:
                # For RSS, get_sources is async, so wrap it with run_async_task
                futures.append(
                    executor.submit(
                        run_async_task,
                        client_module.get_sources(
                            category=category, language=language
                        ),
                    )
                )
            elif key == Channel.NEWSORG:
                # For NewsOrg, get_sources is now async
                futures.append(
                    executor.submit(
                        run_async_task,
                        client_module.get_sources(
                            category=category, country=country, language=language
                        ),
                    )
                )
            else:
                # Fallback for any other synchronous clients (if any in the future)
                futures.append(
                    executor.submit(
                        client_module.get_sources, # Assuming synchronous call
                        category=category,
                        country=country,
                        language=language,
                    )
                )
        for future in as_completed(futures):
            try:
                result = future.result()
                if result: # Ensure result is not None and is iterable
                    sources.extend([r.to_source() for r in result])
            except Exception as e:
                # Handle or log exceptions from futures if necessary
                # print(f"Error fetching sources: {e}")
                pass # For now, just skip if a future fails

    return sources


def get_articles(
    category: Category | None = None,
    country: Country | None = None,
    language: Language | None = None,
    fetch_archived: bool = False,
) -> list[Article]:
    articles = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for key in channels:
            client_module = channels[key].client
            if key == Channel.RSS:
                # For RSS, get_articles is async, so wrap it with run_async_task
                futures.append(
                    executor.submit(
                        run_async_task,
                        client_module.get_articles(
                            category=category, language=language, fetch_archived=fetch_archived
                        ),
                    )
                )
            elif key == Channel.NEWSORG:
                # For NewsOrg, get_articles is now async
                futures.append(
                    executor.submit(
                        run_async_task,
                        client_module.get_articles(
                            category=category, country=country, language=language, fetch_archived=fetch_archived
                        ),
                    )
                )
            else:
                # Fallback for any other synchronous clients (if any in the future)
                futures.append(
                    executor.submit(
                        client_module.get_articles, # Assuming synchronous call
                        category=category,
                        country=country,
                        language=language,
                        # fetch_archived would not be passed to a sync client unless it supports it
                    )
                )
        for future in as_completed(futures):
            try:
                result = future.result()
                if result: # Ensure result is not None and is iterable
                    articles.extend([r.to_article() for r in result])
            except Exception as e:
                # Handle or log exceptions from futures if necessary
                # print(f"Error fetching articles: {e}")
                pass # For now, just skip if a future fails

    return articles


def get_categories() -> list[Category]:
    return [c for c in Category]  # type: ignore
