# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
from functools import singledispatchmethod

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from . import items


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item


class MSDFilterPipeline:
    """
    MSDFilterPipeline is a step to compare with the Million Songs Dataset
    like the paper while extracting."
    """
    def process_item(self, item, spider):
        ...


class JsonLinesWriterPipeline:
    def open_spider(self, spider):
        self.albums = open('albums.jl', 'w')
        self.songs = open('songs.jl', 'w')

    def close_spider(self, spider):
        self.albums.close()
        self.songs.close()

    @singledispatchmethod
    def process_item(self, item, spider):
        pass

    @process_item.register(items.AlbumItem)
    def process_album(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.albums.write(line)
        return item

    @process_item.register(items.SongItem)
    def process_album(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.songs.write(line)
        return item
