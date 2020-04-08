from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


def run_spider(domain: str, start_url: str):
    print(f'Scraping {domain}')

    settings = Settings()
    settings.setmodule('scrapy_spider.offline.settings', priority='project')

    process = CrawlerProcess(settings)
    process.crawl('offline', domain=domain, start_url=start_url)
    process.start()

