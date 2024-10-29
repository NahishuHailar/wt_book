from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi.encoders import jsonable_encoder
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
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    # Retrieve all records
    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    # Create a new record
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # Unpack dict to model fields
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # Update an existing record
    async def update(
        self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # Remove a record
    async def remove(self, db: AsyncSession, id: int) -> ModelType:
        obj = await self.get(db=db, id=id)
        await db.delete(obj)
        await db.commit()
        return obj
