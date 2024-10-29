from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.services.books import book_crud
from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.settings.db import db_handler

router = APIRouter()


# Endpoint to create a new book
@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    return await book_crud.create(db, book)


# Endpoint to get a book by ID
@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    book = await book_crud.get(db, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


# Endpoint to get all books
@router.get("/", response_model=list[BookRead])
async def get_all_books(db: AsyncSession = Depends(db_handler.get_db)):
    return await book_crud.get_all(db)


# Endpoint to update a book
@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int, book: BookUpdate, db: AsyncSession = Depends(db_handler.get_db)
):
    db_book = await book_crud.get(db, book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return await book_crud.update(db, db_book, book)


# Endpoint to delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    book = await book_crud.get(db, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    await book_crud.remove(db, book_id)
