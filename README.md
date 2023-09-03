# Newspy
### The news client written in Python that fetches and curates the world news across the web.

---
![PyPI - Version](https://img.shields.io/pypi/v/newspy) ![GitHub](https://img.shields.io/github/license/onemoola/newspy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/newspy) ![Static Badge](https://img.shields.io/badge/code%20style-black-000000) ![Codecov](https://img.shields.io/codecov/c/gh/onemoola/newspy) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/onemoola/newspy/release.yml)

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

news_articles = newspy.get_articles()
print(news_articles)
```

## Examples

See the [examples](./examples) directory for more examples.

## Contributing

Want to contribute? Read our [contribution guideline](./CONTRIBUTING.md).
