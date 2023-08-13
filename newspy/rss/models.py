import logging
from dataclasses import dataclass
from enum import Enum

from newspy.shared import utils
from newspy.shared.models import Article, Source, Language, Channel

logger = logging.getLogger(__name__)


@dataclass
class RssArticleMediaContent:
    height: str
    width: str
    url: str
    medium: str | None


@dataclass
class RssArticleContent:
    base: str
    value: str


class RssCategory(str, Enum):
    BUSINESS = "business"
    FINANCIAL = "financial"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"


@dataclass
class RssSource:
    id: str
    name: str
    description: str
    url: str
    category: RssCategory
    language: Language

    def to_source(self) -> Source:
        return Source(id=self.id, name=self.name, channel=Channel.RSS)


@dataclass
class RssArticle:
    source: RssSource
    title: str
    description: str
    url: str
    published: str

    def to_article(self) -> Article:
        source = self.source.to_source()

        return Article(
            slug=f"{utils.slugify(source.name)}-{utils.slugify(self.title)}",
            url=self.url,
            url_to_image=None,
            title=self.title,
            abstract=self.description,
            author=None,
            source=source,
            published=utils.to_datetime(self.published),
        )
