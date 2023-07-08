# Newspy

The news client written in Python that fetches and curates the world news across the web.

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

## Local setup

### Install Python and Poetry

```bash
python --version
> Python 3.10.11 # or 3.11.5

poetry --version
> Poetry (version 1.4.2) # or higher
```

### Clone the repository

```bash
git clone https://github.com/onemoola/newspy.git

cd newspy/
```

### Create and activate the virtual environment

```bash
python -m venv .venv

# Activate virtual environment
.venv/bin/activate # Linux or MacOS
.venv/Script/activate # Windows


# Install Newspy
pip install newspy
```

### Install the requirements

```bash
poetry install
```

### Install the git hook scripts

```bash
pre-commit install
```

### Yarn install semantic-release dependencies

```bash
yarn install
```

### Set up husky pre-commit hook

```bash
yarn husky add .husky/commit-msg 'yarn commitlint --edit $1'
```
