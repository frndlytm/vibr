from scrapy.spiders import SitemapSpider

from vibr.scraping.items import AlbumItem, SongItem


class AllMusicSitemapSpider(SitemapSpider):
    name = "allmusic.sitemap"
    sitemap_urls = ["https://www.allmusic.com/sitemap.xml"]
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
            request = response.follow(url + "/attributes", self.parse_song)
            request.meta.update({"_album_": response.url, "track": track})
            yield request

        # Extract album info and yield it to the pipeline stage
        yield AlbumItem(
            _album_=response.url,
            _artist_=response.css("header .album-artist a::attr(href)").get(),
            title=response.css("header .album-title").get(),
            duration=basic_info.css("div.duration span::text").get(),
            genre=basic_info.css("div.genre::text").getall(),
            styles=basic_info.css("div.styles a::text").getall(),
            moods=basic_info.css("div.moods a::text").getall(),
            themes=basic_info.css("div.themes a::text").getall(),
        )

    def parse_song(self, response):
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
