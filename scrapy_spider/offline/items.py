import scrapy


class OfflineResponseItem(scrapy.Item):
    domain = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    mime = scrapy.Field()
