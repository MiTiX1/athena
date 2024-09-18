import certifi

from sys import platform
from pymongo import MongoClient
from pymongo.collection import Collection
from .settings import (
    MONGODB_URL,
    MONGODB_COLLECTION_ARTICLES,
    MONGODB_COLLECTION_BLOGS,
)

from .types_ import ArticleDocument, BlogDocument

if platform == "win32":
    mongo_client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
else:
    mongo_client = MongoClient(MONGODB_URL)

database = mongo_client.get_database()
collection_articles: Collection[ArticleDocument] = database[MONGODB_COLLECTION_ARTICLES]
collection_blogs: Collection[BlogDocument] = database[MONGODB_COLLECTION_BLOGS]