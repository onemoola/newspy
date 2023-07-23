from dataclasses import dataclass
from enum import Enum

from newspy.models import Publication, Publisher, Source
from newspy.shared import utils
from newspy.shared.utils import slugify


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
class NewsorgArticleSourceRes:
    """Newsorg API article source response"""

    status: str
    sources: list[Source]

    def __post_init__(self):
        if isinstance(self.sources, list):
            self.sources = [
                Source(**source) if isinstance(source, dict) else source
                for source in self.sources
            ]


@dataclass
class NewsorgArticle:
    """Newsorg API articles"""

    source: Source
    author: str | None
    title: str
    description: str
    url: str
    urlToImage: str
    publishedAt: str
    content: str

    def __post_init__(self):
        if isinstance(self.source, dict):
            self.source = Source(**self.source)

    def to_publication(self) -> Publication:
        publisher = Publisher(
            id=self.source.id,
            name=self.source.name,
        )

        return Publication(
            slug=f"{slugify(self.source.name)}-{slugify(self.title)}",
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
