# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlbumItem(scrapy.Item):
    _id_ = scrapy.Field()
    title = scrapy.Field()
    genres = scrapy.Field()
    songs = scrapy.Field()


class SongItem(scrapy.Item):
    _id_ = scrapy.Field()
    title = scrapy.Field()
    genres = scrapy.Field()
    styles = scrapy.Field()
    moods = scrapy.Field()
