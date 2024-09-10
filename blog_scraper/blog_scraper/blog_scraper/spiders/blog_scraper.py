import scrapy

from typing import Any, Generator
from scrapy import Request
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from ..items import BlogScraperItem, BlogScraperItemMetadataItem
from ..types_ import ScrapingConfig


class BlogScraperSpider(scrapy.Spider):
    name = "blog_scraper"

    def __init__(self, config: ScrapingConfig, *args: Any, **kwargs: Any):
        self.config = config
        super(BlogScraperSpider, self).__init__(*args, **kwargs)

    def start_requests(self) -> Generator[SeleniumRequest | Request, Any, None]:
        if self.config.get("isSelenium", False):
            yield SeleniumRequest(url=self.config.get("startUrl"), callback=self.parse)
        yield Request(url=self.config.get("startUrl"), callback=self.parse)

    def parse(self, response: Response) -> Generator[SeleniumRequest | Request, Any, None]:
        links = response.css(self.config.get("selectors").get("link"))
        for link in links.css("a::attr(href)").getall():
            if self.config.get("isSelenium", False):
                yield SeleniumRequest(url=response.urljoin(link), callback=self.parse_article)
            yield Request(url=response.urljoin(link), callback=self.parse_article)

    def get_metadata_content(self, response: Response, property_: str) -> str | None:
        content = response.xpath(f"//meta[@property='{property_}']/@content").extract_first()
        if content is None:
            content = response.xpath(f"//meta[@name='{property_}']/@content").extract_first()
        return " ".join(content.split()) if content else None

    def parse_metadata(self, response: Response) -> BlogScraperItemMetadataItem:
        item = BlogScraperItemMetadataItem()

        item["title"] = response.xpath('//title/text()').get()
        item["description"] = self.get_metadata_content(response, "description")
        item["keywords"] = self.get_metadata_content(response, "keywords")

        item["ogTitle"] = self.get_metadata_content(response, "og:title")
        item["ogDescription"] = self.get_metadata_content(response, "og:description")
        item["ogImage"] = self.get_metadata_content(response, "og:image")

        item["twitterTitle"] = self.get_metadata_content(response, "twitter:title")
        item["twitterDescription"] = self.get_metadata_content(response, "twitter:description")
        item["twitterImage"] = self.get_metadata_content(response, "twitter:image")

        return item

    def parse_article(self, response: Response):
        item = BlogScraperItem()
        item["url"] = str(response.url)

        title_css = self.config.get("selectors").get("title").get("cssSelector")
        text_css = self.config.get("selectors").get("text").get("cssSelector")
        date_css = self.config.get("selectors").get("date").get("cssSelector")

        item["title"] = response.css(f"{title_css} *::text").getall()
        item["date"] = response.css(f"{date_css} *::text").getall()
        item["text"] = response.css(f"{text_css} *::text").getall()
        item["metadata"] = self.parse_metadata(response)
        item["imagePath"] = item["metadata"]["ogImage"] or item["head"]["twitterImage"]
        yield item
