# Offline Web

Browse the internet while offline! Built for when I was facing a few weeks without internet and I wanted some good blogs to explore/read. This split into two parts: scrapping, and viewing.


# Scrapping

Uses Scrapy. Give a seed URL and the distributed scraper will go and crawl the site. Only scrapes URLs within the original domain, but will fetch static assets (images/js/css) outside the original domain. Modifies all HTML anchor tags to point where the local copy will be kept.

# Viewing

Uses Django. Provides a webserver to view the underlying scrapped domains from localhost, enabling browsing without internet access.


