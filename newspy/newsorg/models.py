from dataclasses import dataclass, field
from enum import Enum

from newspy.shared import utils
from newspy.shared.models import (
    Article,
    Source,
    Country,
    Language,
    Channel,
)


class NewsorgEndpoint(str, Enum):
    EVERYTHING = "EVERYTHING"
    TOP_HEADLINES = "TOP_HEADLINES"


class NewsorgCategory(str, Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"


@dataclass
class NewsorgArticlesReq:
    """Newsorg API article requests"""

    url: str
    params: dict | None = None


@dataclass
class NewsorgSource:
    name: str
    id: str | None = field(default=None)
    description: str | None = field(default=None)
    url: str | None = field(default=None)
    category: NewsorgCategory | None = field(default=None)
    language: Language | None = field(default=None)
    country: Country | None = field(default=None)

    def to_source(self) -> Source:
        return Source(id=self.id, name=self.name, channel=Channel.NEWSORG)


@dataclass
class NewsorgSourceRes:
    """Newsorg API article source response"""

    status: str
    sources: list[NewsorgSource]

    def __post_init__(self):
        if isinstance(self.sources, list):
            self.sources = [
                NewsorgSource(**source) if isinstance(source, dict) else source
                for source in self.sources
            ]


@dataclass
class NewsorgArticle:
    """Newsorg API articles"""

    source: NewsorgSource
    author: str | None
    title: str
    description: str
    url: str
    urlToImage: str
    publishedAt: str
    content: str

    def __post_init__(self):
        if isinstance(self.source, dict):
            self.source = NewsorgSource(**self.source)

    def to_article(self) -> Article:
        source = self.source.to_source()

        return Article(
            slug=f"{utils.slugify(self.source.name)}-{utils.slugify(self.title)}",
            url=self.url,
            url_to_image=self.urlToImage,
            title=self.title,
            abstract=self.description,
            author=self.author,
            source=source,
            published=utils.to_datetime(self.publishedAt),
        )


@dataclass
class NewsorgArticlesRes:
    """Response from the Newsorg API"""

    status: str
    totalResults: int
    articles: list[NewsorgArticle]

    def __post_init__(self):
        if isinstance(self.articles, list):
            self.articles = [
                NewsorgArticle(**article) if isinstance(article, dict) else article
                for article in self.articles
            ]
