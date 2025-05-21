import asyncio
import csv
import gzip
import io
from pathlib import Path
from typing import NewType

from newspy.models import Category
from newspy.rss.models import RssSource, RssArticle
from newspy.shared.http_client import HttpClient, HttpMethod, ContentType

URL = NewType("URL", str)


async def get_articles(
    category: Category | None = None,
    language: str | None = None,
    sources: list[RssSource] | None = None,
    http_client: HttpClient | None = None,
    fetch_archived: bool = False,
    **kwargs,
) -> list[RssArticle]:
    if not sources:
        # Pass the http_client instance down if provided
        sources = await get_sources(
            category=category, language=language, http_client=http_client, **kwargs
        )

    articles: list[RssArticle] = [] # Ensure articles is typed for clarity
    
    async def _fetch_articles_and_archive(client_to_use: HttpClient):
        # Step 1: Fetch base article data (current logic)
        feed_fetch_tasks = [
            client_to_use.send(
                method=HttpMethod.GET,
                url=source.url,
                headers={"Content-Type": ContentType.XML},
            )
            for source in sources
        ]
        feed_results = await asyncio.gather(*feed_fetch_tasks, return_exceptions=True)

        initial_articles: list[RssArticle] = []
        for i, res in enumerate(feed_results):
            if isinstance(res, Exception) or res is None:
                # Optionally log the error for this feed
                # print(f"Error fetching feed {sources[i].url}: {res}")
                continue

            current_source = sources[i]
            for article_data in res:
                initial_articles.append(
                    RssArticle(
                        source=current_source,
                        title=article_data["title"],
                        description=article_data["description"],
                        url=article_data["url"],
                        published=article_data["published"],
                        # archived_data will be filled next if fetch_archived is True
                    )
                )
        
        if not fetch_archived or not initial_articles:
            return initial_articles

        # Step 2: Fetch archived data if requested
        from newspy.archiver import fetch_from_archivemd # Import here to avoid circular deps at module level

        archive_fetch_tasks = [
            fetch_from_archivemd(article.url, client_to_use) for article in initial_articles
        ]
        archived_results = await asyncio.gather(*archive_fetch_tasks, return_exceptions=True)

        for i, article in enumerate(initial_articles):
            archived_data = archived_results[i]
            if isinstance(archived_data, Exception):
                # Optionally log the exception or store minimal error info
                # print(f"Error fetching archive for {article.url}: {archived_data}")
                article.archived_data = {"status": "failed", "error": str(archived_data)}
            else:
                article.archived_data = archived_data
        
        return initial_articles

    if http_client:
        articles = await _fetch_articles_and_archive(http_client)
    else:
        async with HttpClient() as client_instance:
            articles = await _fetch_articles_and_archive(client_instance)

    return articles


async def get_sources(
    category: Category | None = None,
    language: str | None = None,
    file_path: (Path | URL) = URL(
        "https://github.com/onemoola/newspy/blob/main/data/rss_sources.csv.gz?raw=true"
    ),
    http_client: HttpClient | None = None,
    **kwargs,
) -> list[RssSource]:
    file_content_bytes = None
    if isinstance(file_path, str) and file_path.startswith(("http://", "https://")):
        if http_client:
            file_content_bytes = await http_client.send(
                method=HttpMethod.GET,
                url=file_path,
                headers={"Content-Type": "application/octet-stream"},
            )
        else:
            async with HttpClient() as client_instance:
                file_content_bytes = await client_instance.send(
                    method=HttpMethod.GET,
                    url=file_path,
                    headers={"Content-Type": "application/octet-stream"},
                )
        if not file_content_bytes:
            return []
        file_content = io.BytesIO(file_content_bytes)
    elif isinstance(file_path, Path):
        file_content = file_path # gzip.open can handle a Path object directly
    else:
        # Assuming file_path is a URL string for a local file, which is unusual
        # or an unsupported type. Defaulting to trying to open as local path.
        try:
            file_content = Path(file_path)
            if not file_content.exists(): # Check if local file exists
                 return []
        except TypeError: # Handle cases where Path cannot be constructed
            return []


    # The gzip.open and csv.DictReader part is synchronous.
    # If file_content is a BytesIO, gzip.open can handle it directly (it expects a filename or a file-like object).
    # If file_content is a Path, gzip.open handles opening the file.
    try:
        # When file_content is BytesIO, it's already in memory.
        # When file_content is a Path, gzip.open opens the file from the filesystem.
        with gzip.open(file_content, "rt", encoding="utf-8") as f:
            # csv.DictReader expects a text stream, which `gzip.open` in "rt" mode provides.
            reader = csv.DictReader(f)
            sources_data = list(reader) # Read all data to avoid issues with closed stream if any

        sources = []
        for row in sources_data:
            match_category = (not category) or (row.get("category") == category)
            match_language = (not language) or (row.get("language") == language)
            
            if match_category and match_language:
                try:
                    # Ensure only valid keys for RssSource are passed
                    valid_keys = RssSource.__fields__.keys()
                    filtered_row = {k: v for k, v in row.items() if k in valid_keys}
                    sources.append(RssSource(**filtered_row))
                except TypeError as e:
                    # Skip rows that don't match the RssSource model after filtering
                    # Optionally, log this error: print(f"Skipping row due to TypeError: {row}, {e}")
                    pass
                except Exception as e:
                    # Catch any other unexpected error during RssSource instantiation
                    # Optionally, log this error: print(f"Skipping row due to Error: {row}, {e}")
                    pass

    except (gzip.BadGzipFile, FileNotFoundError, TypeError, EOFError) as e:
        # Handle issues with gzipped file, if file_path was not resolvable, or empty/corrupt file
        # Optionally, log this error: print(f"Error processing sources file: {e}")
        return []

    return sources
