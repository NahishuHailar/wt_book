from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

from .base_crud import CRUDBase


# CRUD class for Book model with additional search methods
class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    # Custom method to find books by tag
    async def get_books_by_tag(self, session: AsyncSession, tag_name: str):
        result = await session.execute(
            select(Book).join(Book.tags).where(Book.tags.any(name=tag_name))
        )
        return result.scalars().all()


# Instantiate the CRUD class for use in API routes
book_crud = CRUDBook(Book)
