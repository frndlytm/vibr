import scrapy
from scrapy.spiders import SitemapSpider


class AllmusicSpider(SitemapSpider):
    name = "allmusic"
    sitemap_urls = ["https://www.allmusic.com/sitemap.xml"]
    allowed_domains = ['allmusic.com']
    sitemap_rules = [
        ("/song/", "parse_song",),
    ]

    def parse_song(self, response):
        pass
