from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from slugify import slugify

from newspy import utils


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


class Category(str, Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"


class Language(str, Enum):
    AR = "ar"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    HE = "he"
    IT = "it"
    NL = "nl"
    NO = "no"
    PT = "pt"
    RU = "ru"
    SV = "sv"
    UD = "ud"
    ZH = "zh"


class Country(str, Enum):
    AE = "ae"
    AR = "ar"
    AT = "at"
    AU = "au"
    BE = "be"
    BG = "bg"
    BR = "br"
    CA = "ca"
    CH = "ch"
    CO = "co"
    CU = "cu"
    CZ = "cz"
    DE = "de"
    EG = "eg"
    FR = "fr"
    GB = "gb"
    GR = "gr"
    HK = "hk"
    HU = "hu"
    ID = "id"
    IE = "ie"
    IL = "il"
    IN = "in"
    IT = "it"
    JP = "jp"
    KR = "kr"
    LT = "lt"
    LV = "lv"
    MA = "ma"
    MX = "mx"
    MY = "my"
    NG = "ng"
    NL = "nl"
    NO = "no"
    NZ = "nz"
    PH = "ph"
    PL = "pl"
    PT = "pt"
    RO = "ro"
    RS = "rs"
    RU = "ru"
    SA = "sa"
    SE = "se"
    SG = "sg"
    SI = "si"
    SK = "sk"
    TH = "th"
    TR = "tr"
    TW = "tw"
    UA = "ua"
    US = "us"
    VE = "ve"
    ZA = "za"


class ArticlesReq(BaseModel):
    """News API article requests"""

    url: str
    params: dict | None = None


class Source(BaseModel):
    """News API article source"""

    id: str | None = None
    name: str
    description: str | None = None
    url: str | None = None
    category: str | None = None
    language: str | None = None
    country: str | None = None


class ArticleSourceRes(BaseModel):
    """News API article source response"""

    status: str
    sources: list[Source]


class Article(BaseModel):
    """News API articles"""

    source: Source
    author: str | None
    title: str
    description: str
    url: str
    url_to_image: str = Field(alias="urlToImage")
    published_at: str = Field(alias="publishedAt")
    content: str

    def to_publication(self) -> Publication:
        publisher = Publisher(
            id=self.source.id if self.source.id else None,
            name=self.source.name,
        )

        return Publication(
            slug=f"{slugify(self.source.name)}-{slugify(self.title)}",
            url=self.url,
            url_to_image=self.url_to_image,
            title=self.title,
            abstract=self.description,
            author=self.author if self.author else None,
            publisher=publisher,
            published=utils.to_datetime(self.published_at),
        )


class ArticlesRes(BaseModel):
    """Response from the News API"""

    status: str
    totalResults: int
    articles: list[Article]
