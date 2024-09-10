from typing import TypedDict, Iterable, NotRequired
from bson import ObjectId
from datetime import datetime


class ScrapingConfigSelectorConfig(TypedDict):
    cssSelector: str
    remove: NotRequired[Iterable[str]]
    takeBefore: NotRequired[str]
    takeAfter: NotRequired[str]


class ScrapingConfigSelector(TypedDict):
    link: str
    title: ScrapingConfigSelectorConfig
    text: ScrapingConfigSelectorConfig
    date: ScrapingConfigSelectorConfig


class ScrapingConfig(TypedDict):
    name: str
    lang: str
    startUrl: str
    isSelenium: bool
    selectors: ScrapingConfigSelector

class BlogDocumentSelector(TypedDict):
    cssSelector: str
    remove: NotRequired[Iterable[str]]
    takeBefore: NotRequired[str]
    takeAfter: NotRequired[str]


class BlogDocumentSelectors(TypedDict):
    link: str
    title: BlogDocumentSelector
    text: BlogDocumentSelector
    date: BlogDocumentSelector


class BlogDocument(TypedDict):
    _id: ObjectId
    name: str
    lang: str
    startUrl: str
    isSelenium: str
    selectors: BlogDocumentSelector
    createdAt: datetime
    updatedAt: datetime
    isDeleted: bool

class ArticleDocumentMetadata(TypedDict):
    title: str | None
    description: str | None
    keywords: str | None
    ogTitle: str | None
    ogDescription: str | None
    ogImage: str | None
    twitterTitle: str | None
    twitterDescription: str | None
    twitterImage: str | None


class ArticleDocument(TypedDict):
    _id: ObjectId
    url: str
    title: str
    date: str
    formatedDate: str | None
    text: str
    imagePath: str | None
    metadata: ArticleDocumentMetadata
    isDeleted: bool