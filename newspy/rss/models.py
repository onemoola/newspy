import logging
from dataclasses import dataclass

from slugify import slugify

from newspy.models import Publication, Publisher
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
class RssArticle:
    id: str
    title: str
    links: list[dict]
    media_content: list[RssArticleMediaContent]
    content: list[RssArticleContent]
    published: str

    def to_publication(self, publisher: Publisher) -> Publication:
        try:
            return Publication(
                slug=f"{slugify(publisher.name)}-{slugify(self.title)}",
                url=self.id,
                url_to_image=self.media_content[0].url,
                title=self.title,
                abstract=self.content[0].value,
                author=None,
                publisher=publisher,
                published=utils.to_datetime(self.published),
            )
        except ValueError:
            logger.warning(
                msg=f"Failed to parse the article with title: {self.title}, id: {self.id}, publisher: {publisher.name}"
            )
            pass
