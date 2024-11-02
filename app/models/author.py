import uuid

from sqlalchemy import UUID, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

author_tags = Table(
    "author_tags",
    Base.metadata,
    mapped_column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    mapped_column(
        "author_id",
        UUID(as_uuid=True),
        ForeignKey("author.id"),
        nullable=False,
    ),
    mapped_column(
        "tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), nullable=False
    ),
)


class Author(Base):
    __tablename__ = "author"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=True)

    books = relationship("Book", back_populates="author")
    tags = relationship("Tag", secondary=author_tags, back_populates="authors")
