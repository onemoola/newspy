import logging
from dataclasses import dataclass

from newspy.shared.models import Publication, Publisher, Source, Language, Category
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

    def to_publisher(self) -> Publisher:
        return Publisher(id=self.id, name=self.name, source=Source.RSS)


@dataclass
class RssArticle:
    title: str
    description: str
    url: str
    published: str

    def to_publication(self, publisher: Publisher) -> Publication:
        try:
            return Publication(
                slug=f"{utils.slugify(publisher.name)}-{utils.slugify(self.title)}",
                url=self.url,
                url_to_image=None,
                title=self.title,
                abstract=self.description,
                author=None,
                publisher=publisher,
                published=utils.to_datetime(self.published),
            )
        except ValueError:
            logger.warning(
                msg=f"Failed to parse the article with title: {self.title}, publisher: {publisher.name}"
            )
            pass


@dataclass
class RssArticleRes:
    sources: list[RssSource]

    def __post_init__(self):
        if isinstance(self.sources, list):
            self.sources = [
                RssSource(**source) if isinstance(source, dict) else source
                for source in self.sources
            ]
