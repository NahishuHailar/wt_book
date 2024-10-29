from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Tag(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)

    books = relationship("Book", secondary="book_tags", back_populates="tags")
    authors = relationship("Author", secondary="author_tags", back_populates="tags")
