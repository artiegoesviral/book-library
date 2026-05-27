from pydantic import BaseModel
from enum import Enum

class MediaType(str, Enum):
    BOOK = "book"
    COMIC = "comic"

class ItemFormat(str, Enum):
    PHYSICAL = "physical"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"

class LibraryItemCreate(BaseModel):
    title: str
    author: str
    genre: str
    media_type: MediaType
    read: bool
    format: ItemFormat


class LibraryItemResponse(LibraryItemCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True