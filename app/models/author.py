from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

author_tags = Table(
    "author_tags",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Author(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=True)

    books = relationship("Book", back_populates="author")
    tags = relationship("Tag", secondary=author_tags, back_populates="authors")
