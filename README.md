# Newspy

The news client written in Python that fetches and curates the world news across the web.

## Table of contents

- [Requirements](#requirements)
- [News Sources](#news-sources)
- [Basic usage](#basic-usage)
    - [Create virtual environment](#create-virtual-environment)
    - [Get the news](#get-the-news)
- [Local setup](#local-setup)
    - [Install Python and Poetry](#install-python-and-poetry)
    - [Clone the repository](#clone-the-repository)
    - [Create and activate the virtual environment](#create-and-activate-the-virtual-environment)
    - [Install the requirements](#install-the-requirements)
    - [Install the git hook scripts](#install-the-git-hook-scripts)
    - [Yarn install semantic-release dependencies](#yarn-install-semantic-release-dependencies)
    - [Set up husky pre-commit hook](#set-up-husky-pre-commit-hook)

## Requirements

* Python 3.10+
* Poetry 1.4.0+ (for dependency management)
* yarn (for the semantic-release versioning)
* API Key from the New API Organisation: https://newsapi.org/

## News Sources

- [X] News API. Requires API Key from: https://newsapi.org/
- [ ] RSS feeds

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

### Get the news

```python
from newspy import Newspy

newsorg_key = "YOUR_NEWSORG_KEY"

client = Newspy(newsorg_key=newsorg_key)
client.publications()
```

## Contributing

Want to contribute? Read our [contribution guideline](./CONTRIBUTING.md).
