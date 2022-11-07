# Newspy

The news client written in Python that fetches and curates the world news across the web.

## Requirements

* Python 3.10
* yarn (for the semantic-release versioning)
* API Key from the New API Organisation: https://newsapi.org/

## News Sources

- [X] News API. Requires API Key from: https://newsapi.org/
- [ ] Twitter
- [ ] RSS feeds

## Getting started

1. Install and confirm the Python version

```bash
python --version
```

2. Create the virtual environment

```bash
python -m venv .venv

# Activate virtual environment
.venv/bin/activate # Linux or MacOS
.venv/Script/activate # Windows
```

3. Install the requirements

```bash
pip install -r requirements-dev.txt
```

4. Install the git hook scripts

```bash
pre-commit install
```

5. Yarn install semantic-release dependencies

```bash
yarn install
```

6. Set up husky pre-commit hook

```bash
yarn husky add .husky/commit-msg 'yarn commitlint --edit $1'
```

## Chores

- [X] Add GitHub Action for Continuous Integration (CI)
- [ ] Add GitHub Action for Continuous Deployment (CD)
