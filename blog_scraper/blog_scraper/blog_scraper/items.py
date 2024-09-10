import scrapy


class BlogScraperItemMetadataItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    ogTitle = scrapy.Field()
    ogDescription = scrapy.Field()
    ogImage = scrapy.Field()
    twitterTitle = scrapy.Field()
    twitterDescription = scrapy.Field()
    twitterImage = scrapy.Field()


class BlogScraperItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    formatedDate = scrapy.Field()
    imagePath = scrapy.Field()
    metadata = scrapy.Field()