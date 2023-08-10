from dataclasses import dataclass, field
from enum import Enum

from newspy.shared import utils
from newspy.shared.models import (
    Publication,
    Publisher,
    Source,
    Country,
    Language,
)


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

    def to_publisher(self) -> Publisher:
        return Publisher(id=self.id, name=self.name, source=Source.NEWSORG)


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

    def to_publication(self) -> Publication:
        publisher = Publisher(
            id=self.source.id,
            name=self.source.name,
            source=Source.NEWSORG,
        )

        return Publication(
            slug=f"{utils.slugify(self.source.name)}-{utils.slugify(self.title)}",
            url=self.url,
            url_to_image=self.urlToImage,
            title=self.title,
            abstract=self.description,
            author=self.author,
            publisher=publisher,
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
