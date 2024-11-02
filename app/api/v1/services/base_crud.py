from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.base import Base

# Type variables for model and schema types
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


# Base CRUD class for common CRUD operations
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # Retrieve a single record by ID
    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        result = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()

    # Retrieve all records
    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    # Create a new record
    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # Unpack dict to model fields
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    # Update an existing record
    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    # Remove a record
    async def remove(self, session: AsyncSession, id: int) -> ModelType:
        obj = await self.get(session=session, id=id)
        await session.delete(obj)
        await session.commit()
        return obj
