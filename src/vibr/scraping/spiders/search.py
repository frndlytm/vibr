import logging
import os

import pandas as pd
import scrapy
from urllib.parse import quote

from vibr.scraping.constants import DATADIR


def handle_artist(spider, response):
    # ArtistItem
    return {
        "artist_id": response.url,
        "name": response.css("h1.artist-name::text").get().strip(),
        "moods": response.css("section.moods a::text").getall(),
        "themes": response.css("section.themes a::text").getall(),
    }


def handle_album(spider, response):
    basic_info = response.css("section.basic-info")
    # Extract album info and yield it to the pipeline stage
    return {
        "album_id": response.url,
        "artist_id": response.css("h2.album-artist a::attr(href)").get(),
        "title": response.css("h1.album-title::text").get(),
        "duration": basic_info.css("div.duration span::text").get(),
        "genres": basic_info.css("div.genre a::text").getall(),
        "styles": basic_info.css("div.styles a::text").getall(),
        "moods": response.css("section.moods a::text").getall(),
        "themes": basic_info.css("div.themes a::text").getall(),
    }


def handle_song(spider, response):
    attributes = response.css("section.attributes")

    return {
        "song_id": "/".join(response.url.split("/")[:-1]),
        "album_id": response.meta["album"],
        "tracknum": response.meta["track"].css("td.tracknum::text").get(),
        "title": response.meta["track"].css("div.title a::text").get(),
        "duration": response.meta["track"].css("td.time::text").get(),
        "genres": attributes.css("div.attribute-tab-genres a::text").getall(),
        "styles": attributes.css("div.attribute-tab-styles a::text").getall(),
        "moods": attributes.css("div.attribute-tab-moods a::text").getall(),
        "themes": attributes.css("div.attribute-tab-themes a::text").getall(),
    }


class AllMusicSpider(scrapy.Spider):
    allowed_domains = ["allmusic.com"]

    def follow_artist(self, response):
        yield handle_artist(self, response)

        # Follow through /discography to scrape albums
        yield response.follow(response.url + "/discography", self.follow_discography)

    def follow_discography(self, response):
        discography = response.css("section.discography table tr")
        urls = discography.css("td.title a::attr(href)").getall()
        yield from response.follow_all(urls, self.follow_album)

    def follow_album(self, response):
        # Extract all track-level info
        yield handle_album(self, response)

        tracks = response.css("section.track-listing")
        for track in tracks.css("table tr.track"):
            if (url := track.css("div.title a::attr(href)").get()):
                request = response.follow(url + "/attributes", self.follow_song)
                request.meta.update({"album": response.url, "track": track})
                yield request

    def follow_song(self, response):
        yield handle_song(self, response)


class AllMusicSearchSpider(AllMusicSpider):
    name = "allmusic.search"

    def start_requests(self):
        metadata = pd.read_csv(os.path.join(DATADIR, "metadata.csv"))
        for artist in metadata.artist_name.unique().tolist():
            url = f"https://www.allmusic.com/search/artists/{quote(artist)}"
            yield scrapy.Request(url, self.follow_top_result)

    def follow_top_result(self, response):
        href = response.css("ul.search-results a::attr(href)").get()
        if href:
            yield response.follow(href, self.follow_artist)
        else:
            self.logger.error(href)


class AllMusicAlbumSpider(AllMusicSpider):
    name = "allmusic.album"

    def start_requests(self):
        url = f"https://www.allmusic.com/album/{quote(self.album_id)}"
        yield scrapy.Request(url, self.follow_album)
