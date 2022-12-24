import logging

from pydantic import BaseModel
from slugify import slugify

from newspy.models import Publication, Publisher
from newspy.shared import utils

logger = logging.getLogger(__name__)


class ArticleMediaContent(BaseModel):
    height: str
    width: str
    url: str
    medium: str | None


class ArticleContent(BaseModel):
    base: str
    value: str


class Article(BaseModel):
    id: str
    title: str
    links: list[dict]
    media_content: list[ArticleMediaContent]
    content: list[ArticleContent]
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
