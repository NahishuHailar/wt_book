# app/api/genres.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db.database import get_db
from app.models.book import Genre
from app.schemas.genre import GenreCreate, GenreUpdate, GenreRead

router = APIRouter()

@router.post("/", response_model=GenreRead)
async def create_genre(genre: GenreCreate, db: AsyncSession = Depends(get_db)):
    new_genre = Genre(**genre.dict())
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)
    return new_genre

@router.get("/{genre_id}", response_model=GenreRead)
async def read_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Genre)
        .options(selectinload(Genre.books))  # Предварительная загрузка книг
        .where(Genre.id == genre_id)
    )
    genre = result.scalars().first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.put("/{genre_id}", response_model=GenreRead)
async def update_genre(genre_id: int, genre: GenreUpdate, db: AsyncSession = Depends(get_db)):
    db_genre = await db.get(Genre, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    for key, value in genre.dict(exclude_unset=True).items():
        setattr(db_genre, key, value)
    await db.commit()
    await db.refresh(db_genre)
    return db_genre

@router.delete("/{genre_id}", response_model=GenreRead)
async def delete_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    db_genre = await db.get(Genre, genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    await db.delete(db_genre)
    await db.commit()
    return db_genre
