from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    model_config = ConfigDict(from_attributes=True)


class TagRead(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TagUpdate(BaseModel):
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
