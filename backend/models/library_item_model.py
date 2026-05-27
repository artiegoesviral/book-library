from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from db import Base
import enum

class MediaType(str, enum.Enum):
    BOOK = "book"
    COMIC = "comic"

class ItemFormat(str, enum.Enum):
    PHYSICAL = "physical"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"


class LibraryItem(Base):
    __tablename__ = "library_items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=False)

    media_type = Column(Enum(MediaType), nullable=False)

    read = Column(Boolean, default=False)

    format = Column(Enum(ItemFormat), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"))