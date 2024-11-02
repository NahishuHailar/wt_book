import uuid

from sqlalchemy import UUID, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

book_tags = Table(
    "book_tags",
    Base.metadata,
    mapped_column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    mapped_column(
        "book_id", UUID(as_uuid=True), ForeignKey("book.id"), nullable=False
    ),
    mapped_column(
        "tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), nullable=False
    ),
)


class Book(Base):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    published_year: Mapped[int] = mapped_column(Integer, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    tags = relationship("Tag", secondary=book_tags, back_populates="books")
