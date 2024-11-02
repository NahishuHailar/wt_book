from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.services.tags import tag_crud
from app.schemas.tag import TagCreate, TagRead, TagUpdate
from app.settings.db import db_handler

router = APIRouter()


# Endpoint to create a new tag
@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate, session: AsyncSession = Depends(db_handler.get_db)
):
    return await tag_crud.create(session, tag)


# Endpoint to get a tag by ID
@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(
    tag_id: int, session: AsyncSession = Depends(db_handler.get_db)
):
    tag = await tag_crud.get(session, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


# Endpoint to get all tags
@router.get("/", response_model=list[TagRead])
async def get_all_tags(session: AsyncSession = Depends(db_handler.get_db)):
    return await tag_crud.get_all(session)


# Endpoint to update a tag
@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: int,
    tag: TagUpdate,
    session: AsyncSession = Depends(db_handler.get_db),
):
    db_tag = await tag_crud.get(session, tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return await tag_crud.update(session, db_tag, tag)


# Endpoint to delete a tag
@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int, session: AsyncSession = Depends(db_handler.get_db)
):
    tag = await tag_crud.get(session, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    await tag_crud.remove(session, tag_id)
