# Newspy

The news client written in Python that fetches and curates the world news across the web.

## Table of contents

- [Requirements](#requirements)
- [News Sources](#news-sources)
- [Basic usage](#basic-usage)
    - [Create virtual environment](#create-virtual-environment)
    - [Get the news from Newsorg API](#get-the-news-from-newsorg-api)
    - [Get the news from RSS Feeds](#get-the-news-from-rss-feeds)
- [Contributing](#contributing)

## Requirements

* Python 3.10+
* Poetry 1.4.0+ (for dependency management)
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

### Get the news from Newsorg API

```python
from newspy import client
from newspy import newsorg
from newspy.newsorg.models import NewsorgEndpoint

newsorg_api_key = "YOUR_NEWSORG_KEY"

client.configure(newsorg_api_key=newsorg_api_key)
newsorg_articles = newsorg.get_articles(
    endpoint=NewsorgEndpoint.TOP_HEADLINES,
    search_text="bitcoin",
)

print(newsorg_articles)
```

### Get the news from RSS Feeds

```python
from newspy import rss

rss_articles = rss.get_articles()

print(rss_articles)
```

## Contributing

Want to contribute? Read our [contribution guideline](./CONTRIBUTING.md).
