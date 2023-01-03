from datetime import datetime

from pydantic import BaseModel


class Publisher(BaseModel):
    """Publisher domain model"""

    id: str | None
    name: str


class Publication(BaseModel):
    """Publication domain model"""

    slug: str
    url: str
    url_to_image: str
    title: str
    abstract: str
    author: str | None
    publisher: Publisher
    published: datetime
