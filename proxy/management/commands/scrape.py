from django.core.management.base import BaseCommand

from scrapy_spider.run_offline_spider import run_spider


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('domain', nargs=1, type=str)
        parser.add_argument('--start_url', '-s', nargs='?', type=str, default=None)

    def handle(self, *args, **options):
        domain = options.get('domain', None)[0]
        start_url = options.get('start_url')
        run_spider(domain, start_url)
