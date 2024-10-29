from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

book_tags = Table(
    "book_tags",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    published_year: Mapped[int] = mapped_column(Integer, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    tags = relationship("Tag", secondary=book_tags, back_populates="books")
