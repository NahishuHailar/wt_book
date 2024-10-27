# app/api/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate, TagRead

router = APIRouter()

@router.post("/", response_model=TagRead)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    new_tag = Tag(**tag.dict())
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag

@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tag)
        .options(selectinload(Tag.books))  # Предварительная загрузка книг
        .where(Tag.id == tag_id)
    )
    tag = result.scalars().first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(tag_id: int, tag: TagUpdate, db: AsyncSession = Depends(get_db)):
    db_tag = await db.get(Tag, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    for key, value in tag.dict(exclude_unset=True).items():
        setattr(db_tag, key, value)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

@router.delete("/{tag_id}", response_model=TagRead)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    db_tag = await db.get(Tag, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    await db.delete(db_tag)
    await db.commit()
    return db_tag
