from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate

from .base_crud import CRUDBase


# CRUD class for Author model with additional search methods
class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    # Custom method to find authors by tag
    async def get_authors_by_tag(self, db: AsyncSession, tag_name: str):
        result = await db.execute(
            select(Author).join(Author.tags).where(Author.tags.any(name=tag_name))
        )
        return result.scalars().all()


# Instantiate the CRUD class for use in API routes
author_crud = CRUDAuthor(Author)
