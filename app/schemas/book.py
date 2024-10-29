from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


class BookBase(BaseModel):
    title: str
    published_year: Optional[int] = None
    author_id: int  # ID автора, поскольку связь многие-к-одному


class BookCreate(BookBase):
    model_config = ConfigDict(from_attributes=True)


class BookRead(BookBase):
    id: int
    # tags: Optional[List[str]] = []
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    published_year: Optional[int] = None
    author_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
