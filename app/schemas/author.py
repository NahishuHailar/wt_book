from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    country: Optional[str] = None


class AuthorCreate(AuthorBase):
    model_config = ConfigDict(from_attributes=True)


class AuthorRead(AuthorBase):
    id: int
    # tags: Optional[List[str]] = []
    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
