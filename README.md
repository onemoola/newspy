# Newspy
### The news client written in Python that fetches and curates the world news across the web.

---
![PyPI - Version](https://img.shields.io/pypi/v/newspy) ![GitHub](https://img.shields.io/github/license/onemoola/newspy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/newspy) ![Static Badge](https://img.shields.io/badge/code%20style-black-000000) ![Codecov](https://img.shields.io/codecov/c/gh/onemoola/newspy) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/onemoola/newspy/main.yml)

---

## Table of contents

- [Requirements](#requirements)
- [News Sources](#news-sources)
- [Basic usage](#basic-usage)
    - [Create virtual environment](#create-virtual-environment)
    - [RSS feeds client](#rss-feeds-client)
    - [Newsorg client](#newsorg-client)
    - [Newspy client](#newspy-client)
- [Contributing](#contributing)

## Requirements

* Python 3.10+
* Poetry 1.4.0+ (for dependency management)
* `aiohttp` (for asynchronous HTTP requests)
* `beautifulsoup4` (for parsing HTML content, e.g., from archives)
* `requests` (for some underlying synchronous operations or by Newsorg client if not fully async yet)
* yarn (for the semantic-release versioning)
* API Key from the New API Organisation: https://newsapi.org/

## News Sources

- [X] News API. Requires API Key from: https://newsapi.org/
- [X] RSS feeds

## Basic usage

### Create virtual environment

```bash
python -m venv .venv

# Activate virtual environment
.venv/bin/activate # Linux or MacOS
.venv/Script/activate # Windows


# Install
pip install newspy
```

### RSS feeds client

#### Get available news sources from RSS feeds

```python
from newspy import rss

rss_sources = rss.get_sources()
print(rss_sources)
```

#### Get articles from RSS feeds

```python
rss_articles = rss.get_articles()
print(rss_articles)
```

### Newsorg client

#### Configure your Newsorg API key

You can get one here: https://newsapi.org/

```python
import newspy.client as newspy

newsorg_api_key = "YOUR_NEWSORG_KEY"
newspy.configure(newsorg_api_key=newsorg_api_key)
```

#### Get available news sources from Newsorg

```python
from newspy import newsorg

newsorg_sources = newsorg.get_sources()
print(newsorg_sources)
```

#### Get articles from Newsorg

```python
from newspy import newsorg
from newspy.newsorg.models import NewsorgEndpoint

newsorg_articles = newsorg.get_articles(
    endpoint=NewsorgEndpoint.TOP_HEADLINES,
    search_text="bitcoin",
)

print(newsorg_articles)
```

### Newspy client

The newspy client makes it convenient to get articles from both the RSS feeds and Newsorg APIs.

#### Configure your Newsapi API key

```python
import newspy.client as newspy

newsorg_api_key = "YOUR_NEWSORG_KEY"
newspy.configure(newsorg_api_key=newsorg_api_key)
```

#### Get available news sources from both RSS feeds and Newsorg

```python
import newspy.client as newspy

news_sources = newspy.get_sources()
print(news_sources)
```

#### Get articles from both RSS feeds and Newsorg

```python
import newspy.client as newspy
from newspy.models import Language # Ensure Language is imported if used

# Example: Fetching articles with archived content
news_articles = newspy.get_articles(
    language=Language.EN, # Or any other parameters
    fetch_archived=True
)

for article in news_articles:
    print(f"Title: {article.title}")
    if article.archived_data and article.archived_data.get('status') == 'success':
        print(f"  Archived URL: {article.archived_data.get('archive_url')}")
        print(f"  Archived Title: {article.archived_data.get('title')}")
        # print(f"  Archived Text: {article.archived_data.get('text')[:200]}...") # Example to print snippet
    elif article.archived_data:
        print(f"  Archiving status: {article.archived_data.get('status')}, Original URL: {article.archived_data.get('original_url')}")
        if article.archived_data.get('error'):
             print(f"  Archiving error: {article.archived_data.get('error')}")
    else:
        print(f"  No archive data fetched for this article.")
    print("-" * 30)

# print(news_articles) # Original print statement
```

The `fetch_archived=True` parameter in `newspy.get_articles()` enables fetching an archived version of each article's content from [archive.md](https://archive.md/).
If successful, `article.archived_data` will be a dictionary containing:
- `original_url`: The URL of the article that was attempted to be archived.
- `archive_url`: The URL of the snapshot on archive.md.
- `title`: The title of the article as extracted from the archive.
- `text`: The main textual content extracted from the archive.
- `status`: Indicates the outcome of the archiving attempt (e.g., "success", "failed").
If the archiving attempt fails, `status` will be "failed", and an `error` key might be present with more details. If `fetch_archived` is `False` (the default), `article.archived_data` will be `None`.

**Note on Asynchronous Operations:**

The underlying clients for RSS (`newspy.rss.client`) and NewsOrg (`newspy.newsorg.client`) now operate asynchronously using `aiohttp` for improved performance when fetching multiple feeds or articles. The main `newspy.client` module conveniently handles the asyncio event loop, so you can call its functions like `newspy.get_articles()` in a synchronous manner as shown in the examples.

## Examples

See the [examples](./examples) directory for more examples.

## Contributing

Want to contribute? Read our [contribution guideline](./CONTRIBUTING.md).
