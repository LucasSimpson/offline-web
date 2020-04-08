import logging
import re

import scrapy

from proxy.models import Document
from scrapy_spider.offline.items import OfflineResponseItem
from scrapy_spider.offline.utils import is_mime_html, format_url


class OfflineScraperSpider(scrapy.Spider):
    name = 'offline'
    domain = ''
    custom_settings = {
        'DEPTH_LIMIT': 0,
    }
    blacklisted_domains = [
        'youtube',
        'facebook',
        'reddit',
        'twitter',
        'instagram',
        'gravatar',
    ]

    def __init__(self, domain=None, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not domain:
            raise Exception('Must provide a domain')

        self.domain = domain
        self.start_urls = [start_url] if start_url else [
            f'http://{self.domain}',
            f'https://{self.domain}',
        ]
        self.log(f'Starting with domain={self.domain}, start_urls={self.start_urls}', level=logging.INFO)

    def get_domain_from_url(self, url):
        url = format_url(url, self.domain, self.domain)

        match = re.match(r'(https?://)?(?P<domain>[^/]*)', url)
        if match:
            return match.group('domain')
        return ''

    def filter_blacklist(self, url) -> bool:
        domain = self.get_domain_from_url(url)

        for blacklisted_domain in self.blacklisted_domains:
            if blacklisted_domain in domain:
                self.log(f'Ignoring {url}, domain {domain} is blacklisted.', level=logging.DEBUG)
                return False

        return True

    def filter_db(self, url) -> bool:
        in_db = Document.objects.filter(url=format_url(url, self.domain)).count() > 0
        if in_db:
            self.log(f'Ignoring {url}, already in DB.', level=logging.DEBUG)
        return not in_db

    def parse_document(self, response, recurse):
        ct = response.headers.get('content-type', '').decode('utf-8')

        # send for processing
        yield OfflineResponseItem(
            domain=self.domain,
            url=format_url(response.url, domain=self.domain),
            body=response.body,
            mime=ct
        )

        # if we got here we only accept HTML docs. All other docs should go through the other parse methods.
        # if we _did_ get here without HTML doc, its cause there was an anchor to another resource - presumably
        # an image or something. in any case we'll still save it through the pipeline, we just don't scan it to continue
        if not is_mime_html(ct):
            return

        requests = []

        # follow all hrefs
        if recurse:
            for link in set(list(response.css('a::attr(href)').getall())):
                link_in_our_domain = self.get_domain_from_url(link) == self.domain

                # if our domain, parse recursively
                if link_in_our_domain:
                    requests += [response.follow(link, self.parse)]

                # if not our domain, just parse the one page if it passes blacklist
                elif self.filter_blacklist(link):
                    requests += [response.follow(link, self.parse_non_recurse)]

        # get all static urls. images, CSS, JS
        static_urls = response.css('img::attr(src)').getall() + \
                      response.xpath('//link[@rel="stylesheet"]').xpath('@href').getall() + \
                      response.xpath('//script').xpath('@src').getall() + \
                      response.xpath('//link[@rel="prefetch"]').xpath('@href').getall()

        # follow all static urls
        for url in static_urls:
            requests += [response.follow(url, self.parse_static)]

        # filter our documents already in DB
        for req in requests:
            if self.filter_db(req.url):
                yield req

    def parse(self, response):
        """parse page + assets, and recursively follow all links"""

        self.log(f'Parsing {response.url} recursively', level=logging.DEBUG)
        for result in self.parse_document(response, True):
            yield result

    def parse_non_recurse(self, response):
        """parse a page + assets."""

        self.log(f'Parsing {response.url} NON-recursively', level=logging.DEBUG)
        for result in self.parse_document(response, False):
            yield result

    def parse_static(self, response):
        """only process that one document."""

        # only thing we do is send for processing
        yield OfflineResponseItem(
            domain=self.domain,
            url=format_url(response.url, domain=self.domain),
            body=response.body,
            mime=response.headers.get('content-type', '').decode('utf-8')
        )
