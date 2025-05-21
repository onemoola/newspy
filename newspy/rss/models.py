import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

from newspy.models import Article, Source, Language, Channel, Category
from newspy.shared import utils

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


@dataclass
class RssSource:
    id: str
    name: str
    description: str
    url: str
    category: Category
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
    archived_data: Optional[Dict[str, Any]] = None

    def to_article(self) -> Article:
        source = self.source.to_source()

        return Article(
            slug=f"{utils.slugify(source.name)}-{utils.slugify(self.title)}",
            url=self.url,
            url_to_image=None, # RSS typically doesn't have a standardized image field
            title=self.title,
            abstract=self.description,
            author=None, # RSS feeds vary widely in how/if they provide author
            source=source,
            published=utils.to_datetime(self.published),
            archived_data=self.archived_data,
        )
