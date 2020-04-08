from bs4 import BeautifulSoup

from proxy.models import Document, Domain
from scrapy_spider.offline.items import OfflineResponseItem
from scrapy_spider.offline.utils import is_mime_html, format_url


def proxy_url(url: str) -> str:
    return f'/proxy/{url}'


def replace_urls(html, domain, current_url, encoding=None):

    soup = BeautifulSoup(html, from_encoding=encoding, features='lxml')

    def find_replace(tag, attr):
        for hit in soup.find_all(tag):
            if hit.get(attr):
                hit[attr] = proxy_url(format_url(hit[attr], domain, current_url))

    # find replace links
    find_replace('a', 'href')
    find_replace('img', 'src')
    find_replace('link', 'href')
    find_replace('script', 'src')

    return soup.prettify('utf-8')


class OfflinePipelineProxyURLs(object):
    def process_item(self, item, spider):

        body = item['body']
        if is_mime_html(item['mime']):
            body = replace_urls(body, item['domain'], item['url'])

        return OfflineResponseItem(
            domain=item['domain'],
            url=item['url'],
            body=body,
            mime=item['mime'],
        )


class OfflinePipelineSaveDocument(object):
    """Save document to DB."""

    def process_item(self, item, spider):
        # domains
        domains = Domain.objects.filter(domain=item['domain'])
        if domains.count() == 0:
            domain = Domain(domain=item['domain'])
            domain.save()
            print(f'Created {domain}')
        else:
            domain = domains[0]

        # delete existing
        existing = Document.objects.filter(url=item['url'])
        if existing.count() > 0:
            for doc in existing:
                doc.delete()

        # create latest
        doc = Document(
            domain=domain,
            url=item['url'],
            content=item['body'],
            mime=item['mime'],
        )
        doc.save()
        print(f'Saved {doc} to DB (mime={doc.mime}, url={doc.url})')



