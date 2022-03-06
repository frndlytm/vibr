import scrapy
from scrapy.spiders import SitemapSpider


class AllmusicSpider(SitemapSpider):
    name = "allmusic"
    sitemap_urls = ["https://www.allmusic.com/sitemap.xml"]
    allowed_domains = ['allmusic.com']
    sitemap_rules = [
        ("/album/", "parse_album",),
    ]

    def parse_album(self, response):
        # Extract album info and yield it to the pipeline stage


        # Get all the songs on the page

        # yield a scrapy.Request(song/:id/attributes, self.parse_song)
        ...

    def parse_song(self, response):
        # Extract attributes

        # yield to pipeline
        ...
