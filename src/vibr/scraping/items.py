# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbumItem(scrapy.Item):
    _artist_ = scrapy.Field()
    _album_ = scrapy.Field()
    title = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    styles = scrapy.Field()
    moods = scrapy.Field()
    themes = scrapy.Field()


class SongItem(scrapy.Item):
    _song_ = scrapy.Field()
    _album_ = scrapy.Field()
    tracknum = scrapy.Field()
    title = scrapy.Field()
    duration = scrapy.Field()
    genres = scrapy.Field()
    styles = scrapy.Field()
    moods = scrapy.Field()
    themes = scrapy.Field()
