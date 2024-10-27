# app/api/books.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db.database import get_db
from app.models.book import Book, Genre
from app.schemas.book import BookCreate, BookUpdate, BookRead

router = APIRouter()

@router.post("/", response_model=BookRead)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    # Найдем указанные жанры в базе данных
    genres = []
    if book.genre_ids:
        result = await db.execute(select(Genre).where(Genre.id.in_(book.genre_ids)))
        genres = result.scalars().all()

    # Создаем книгу с жанрами
    new_book = Book(**book.dict(exclude={"genre_ids"}), genres=genres)
    db.add(new_book)
    await db.commit()

    # Загрузим книгу с жанрами и тегами для сериализации
    result = await db.execute(
        select(Book)
        .options(selectinload(Book.genres), selectinload(Book.tags), selectinload(Book.author))
        .where(Book.id == new_book.id)
    )
    created_book = result.scalars().first()
    return {
        "id": created_book.id,
        "title": created_book.title,
        "price": created_book.price,
        "quantity": created_book.quantity,
        "discount": created_book.discount,
        "author_id": created_book.author_id,
        "genres": [genre.name for genre in created_book.genres],
        "tags": [tag.name for tag in created_book.tags]
    }

@router.get("/{book_id}", response_model=BookRead)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Book)
        .options(selectinload(Book.author), selectinload(Book.genres), selectinload(Book.tags))
        .where(Book.id == book_id)
    )
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {
        "id": book.id,
        "title": book.title,
        "price": book.price,
        "quantity": book.quantity,
        "discount": book.discount,
        "author_id": book.author_id,
        "genres": [genre.name for genre in book.genres],
        "tags": [tag.name for tag in book.tags]
    }

@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=BookRead)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(db_book)
    await db.commit()
    return db_book
