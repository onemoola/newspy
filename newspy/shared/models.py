from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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


class Category(str, Enum):
    BUSINESS = "business"
    FINANCIAL = "financial"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"


class Source(str, Enum):
    """Source domain model"""

    NEWSORG = "newsorg"
    RSS = "rss"


@dataclass
class Publisher:
    """Publisher domain model"""

    id: str | None
    name: str
    source: Source


@dataclass
class Publication:
    """Publication domain model"""

    slug: str
    url: str
    url_to_image: str | None
    title: str
    abstract: str
    author: str | None
    publisher: Publisher
    published: datetime
