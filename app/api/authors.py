# app/api/authors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db.database import get_db
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate, AuthorRead

router = APIRouter()

@router.post("/", response_model=AuthorCreate)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    new_author = Author(**author.dict())
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author

@router.get("/{author_id}", response_model=AuthorRead)
async def read_author(author_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Author)
        .options(selectinload(Author.books))  # Предварительная загрузка книг
        .where(Author.id == author_id)
    )
    author = result.scalars().first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(author_id: int, author: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    db_author = await db.get(Author, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    await db.commit()
    await db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", response_model=AuthorRead)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    db_author = await db.get(Author, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    await db.delete(db_author)
    await db.commit()
    return db_author
