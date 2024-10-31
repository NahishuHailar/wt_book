from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.services.authors import author_crud
from app.schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from app.settings.db import db_handler

router = APIRouter()


# Endpoint to create a new author
@router.post("/", response_model=AuthorCreate, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: AuthorCreate, db: AsyncSession = Depends(db_handler.get_db)
):
    return await author_crud.create(db, author)


# Endpoint to get an author by ID
@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(author_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    author = await author_crud.get(db, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


# Endpoint to get all authors
@router.get("/", response_model=list[AuthorRead])
async def get_all_authors(db: AsyncSession = Depends(db_handler.get_db)):
    return await author_crud.get_all(db)


# Endpoint to update an author
@router.put("/{author_id}", response_model=AuthorUpdate)
async def update_author(
    author_id: int, author: AuthorUpdate, db: AsyncSession = Depends(db_handler.get_db)
):
    db_author = await author_crud.get(db, author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return await author_crud.update(db, db_author, author)


# Endpoint to delete an author
@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    author = await author_crud.get(db, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    await author_crud.remove(db, author_id)
