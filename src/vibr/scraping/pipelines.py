# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import os
from typing import Type

import pydantic
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from . import constants, items


class DropDuplicates:
    model: Type = None

    def __init__(self, model: Type[pydantic.BaseModel]):
        self.seen = set()
        self.model = model

    def process_item(self, item, spider):
        if isinstance(item, self.model):
            adapter = ItemAdapter(item)
            if adapter['id'] in self.seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.seen.add(adapter['id'])
                return item

        else:
            return item


class DropDuplicateAlbums:
    def __init__(self):
        super().__init__(model=items.AlbumItem)


class DropDuplicateArtists:
    def __init__(self):
        super().__init__(model=items.ArtistItem)


class DropDuplicateSongs:
    def __init__(self):
        super().__init__(model=items.SongItem)


class MSDDropPipeline:
    """
    MSDFilterPipeline is a step to compare with the Million Songs Dataset
    like the paper while extracting."
    """
    def process_item(self, item, spider):
        ...


class JsonLinesWriter:
    def __init__(self, path: str, model: Type[pydantic.BaseModel]):
        self.path = path
        self.model = model

    def open_spider(self, spider):
        self.file = open(self.path, "w+")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        try: 
            obj = pydantic.parse_obj_as(self.model, item)
            line = obj.json() + "\n"
            self.file.write(line)
        # except:
        #     logging.exception(f"Failed to parse {str(item)}")
        finally:
            return item


class AlbumJsonLinesWriter(JsonLinesWriter):
    def __init__(self):
        super().__init__(
            path=os.path.join(constants.DATADIR, "raw", "albums.jl"),
            model=items.AlbumItem,
        )


class ArtistJsonLinesWriter(JsonLinesWriter):
    def __init__(self):
        super().__init__(
            path=os.path.join(constants.DATADIR, "raw", "artists.jl"),
            model=items.ArtistItem,
        )


class SongJsonLinesWriter(JsonLinesWriter):
    def __init__(self):
        super().__init__(
            path=os.path.join(constants.DATADIR, "raw", "songs.jl"),
            model=items.SongItem,
        )
