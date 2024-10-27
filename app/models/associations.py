from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.database import Base

book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

author_tags = Table(
    "author_tags",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("authors.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)
