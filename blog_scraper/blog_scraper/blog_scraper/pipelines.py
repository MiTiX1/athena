import re

from dateparser.search import search_dates
from .spiders.blog_scraper import BlogScraperSpider
from .items import BlogScraperItem
from .mongo_provider import collection_articles


class BlogScraperPipeline:
    def format_text(self, text: list[str]) -> str:
        text = " ".join(text)
        text = re.sub('\n|\t|\r', "", text)
        text = re.sub("\s+", " ", text, flags=re.UNICODE)
        return text.strip()

    def clean_text(self, item: BlogScraperItem) -> None:
        item["title"] = self.format_text(item["title"])
        item["text"] = self.format_text(item["text"])
        item["date"] = self.format_text(item["date"])

    def remove_from(self, item: BlogScraperItem, spider: BlogScraperSpider) -> None:
        remove_from_title = spider.config.get("selectors").get("title").get("remove")
        remove_from_text = spider.config.get("selectors").get("text").get("remove")
        remove_from_date = spider.config.get("selectors").get("date").get("remove")

        if remove_from_title:
            for pattern in remove_from_title:
                item["title"] = re.sub(pattern, "", item["title"])

        if remove_from_text:
            for pattern in remove_from_text:
                item["text"] = re.sub(pattern, "", item["text"])

        if remove_from_date:
            for pattern in remove_from_date:
                item["date"] = re.sub(pattern, "", item["date"])

    def take_before(self, item: BlogScraperItem, spider: BlogScraperSpider) -> None:
        take_before_title = spider.config.get("selectors").get("title").get("takeBefore")
        take_before_text = spider.config.get("selectors").get("text").get("takeBefore")
        take_before_date = spider.config.get("selectors").get("date").get("takeBefore")

        if take_before_title:
            prefix, success, _ = item["title"].partition(take_before_title)
            item["title"] = prefix if prefix else success

        if take_before_text:
            prefix, success, _ = item["text"].partition(take_before_text)
            item["text"] = prefix if prefix else success

        if take_before_date:
            prefix, success, _ = item["date"].partition(take_before_date)
            item["date"] = prefix if prefix else success

    def take_after(self, item: BlogScraperItem, spider: BlogScraperSpider) -> None:
        take_after_title = spider.config.get("selectors").get("title").get("takeAfter")
        take_after_text = spider.config.get("selectors").get("text").get("takeAfter")
        take_after_date = spider.config.get("selectors").get("date").get("takeAfter")

        if take_after_title:
            prefix, success, result = item["title"].partition(take_after_title)
            item["title"] = result if success else prefix

        if take_after_text:
            prefix, success, result = item["text"].partition(take_after_text)
            item["text"] = result if success else prefix

        if take_after_date:
            prefix, success, result = item["date"].partition(take_after_date)
            item["date"] = result if success else prefix

    def convert_date(self, item: BlogScraperItem, spider: BlogScraperSpider) -> None:
        try:
            if item["date"]:
                raw_date = " ".join(item["date"]).strip()
                raw_date = re.sub(rf"\/|-|_|\.|\|", " ", raw_date)
                lang = spider.config.get("lang")

                date_searched_as_text = search_dates(raw_date, languages=[lang])

                if date_searched_as_text:
                    parsed = date_searched_as_text[0][1]

                if parsed:
                    item["formatedDate"] = parsed
                else:
                    item["formatedDate"] = None
        except Exception as e:
            item["formatedDate"] = None

    def item_to_dict(self, item: BlogScraperItem) -> dict:
        return {
            "url": item["url"],
            "title": item["title"],
            "date": item["date"],
            "formatedDate": item["formatedDate"],
            "text": item["text"],
            "imagePath": item["imagePath"],
            "metadata": {
                "title": item["metadata"]["title"],
                "description": item["metadata"]["description"],
                "keywords": item["metadata"]["keywords"],
                "ogImage": item["metadata"]["ogImage"],
                "ogTitle": item["metadata"]["ogTitle"],
                "ogDescription": item["metadata"]["ogDescription"],
                "twitterImage": item["metadata"]["twitterImage"],
                "twitterTitle": item["metadata"]["twitterTitle"],
                "twitterDescription": item["metadata"]["twitterDescription"],
            }
        }

    def save_article(self, item: BlogScraperItem) -> None:
        article = collection_articles.find_one({"url": item["url"]})
        if not article:
            article = self.item_to_dict(item)
            article["isDeleted"] = False
            collection_articles.insert_one(article)  # TODO: bulk write

    def process_item(self, item: BlogScraperItem, spider: BlogScraperSpider) -> BlogScraperItem:
        self.clean_text(item)
        self.remove_from(item, spider)
        self.take_before(item, spider)
        self.convert_date(item, spider)
        self.save_article(item)

        return item
