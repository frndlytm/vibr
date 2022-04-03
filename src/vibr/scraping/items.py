# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Optional

import pydantic


class AlbumItem(pydantic.BaseModel):
    album_id: str
    artist_id: Optional[str]   # None means there's no URL, like `Various Artists`
    title: str
    duration: Optional[str]
    genres: list[str] = pydantic.Field(default_factory=list)
    styles: list[str] = pydantic.Field(default_factory=list)
    moods: list[str] = pydantic.Field(default_factory=list)
    themes: list[str] = pydantic.Field(default_factory=list)


class ArtistItem(pydantic.BaseModel):
    artist_id: str
    name: str
    moods: list[str] = pydantic.Field(default_factory=list)
    themes: list[str] = pydantic.Field(default_factory=list)


class SongItem(pydantic.BaseModel):
    song_id: str
    album_id: str
    tracknum: int
    title: str
    duration: str
    genres: list[str] = pydantic.Field(default_factory=list)
    styles: list[str] = pydantic.Field(default_factory=list)
    moods: list[str] = pydantic.Field(default_factory=list)
    themes: list[str] = pydantic.Field(default_factory=list)
