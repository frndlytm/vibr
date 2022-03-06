import scrapy
from scrapy.spiders import SitemapSpider

from vibr.scraping.items import AlbumItem, SongItem


class AllmusicSpider(SitemapSpider):
    name = "allmusic"
    sitemap_urls = ["https://www.allmusic.com/sitemaps/sitemap-32.xml"]
    allowed_domains = ['allmusic.com']
    sitemap_rules = [
        ("/album/", "parse_album",),
    ]

    def parse_album(self, response):
        basic_info = response.css("section.basic-info")
        tracks = response.css("section.track-listing")

        # Extract all track-level info
        for track in tracks.css("table tr.track"):
            url = track.css("div.title a::attr(href)").get()
            request = response.follow(url + "/attributes", self.parse_song_attributes)
            request.meta.update({"_album_": response.url, "track": track})
            yield request

        # Extract album info and yield it to the pipeline stage
        yield AlbumItem(
            _album_=response.url,
            _artist_=response.css("header .album-artist a::attr(href)").get(),
            title=basic_info.css(".album-title").get(),
            genre=basic_info.xpath("//div[@class='genre']/text()").get(),
            duration=basic_info.xpath("//div[@class='duration']/span/text()").get(),
            styles=basic_info.xpath("//div[@class='styles']/*/a/text()").getall(),
            moods=basic_info.xpath("//div[@class='moods']/*/a/text()").getall(),
            themes=basic_info.xpath("//div[@class='themes']/*/a/text()").getall(),
        )

    def parse_song_attributes(self, response):
        attributes = response.css("section.attributes")

        yield SongItem(
            _song_="/".join(response.url.split("/")[:-1]),
            _album_=response.meta["_album_"],
            tracknum=response.meta["track"].css("td.tracknum::text").get(),
            title=response.meta["track"].css("div.title a::text").get(),
            duration=response.meta["track"].css("td.time::text").get(),
            genres=attributes.css("div.attribute-tabs-genres a::text").getall(),
            styles=attributes.css("div.attribute-tabs-styles a::text").getall(),
            moods=attributes.css("div.attribute-tabs-moods a::text").getall(),
            themes=attributes.css("div.attribute-tabs-moods a::text").getall(),
        )
