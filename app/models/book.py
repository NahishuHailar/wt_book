from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base

from app.models.associations import book_tags, book_genres


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    discount = Column(Float, default=0.0)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")
    tags = relationship("Tag", secondary="book_tags", back_populates="books")
    genres = relationship("Genre", secondary="book_genres", back_populates="books")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary="book_genres", back_populates="genres")
