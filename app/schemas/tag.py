# app/schemas/tag.py
from pydantic import BaseModel

# Базовая схема для тега
class TagBase(BaseModel):
    name: str

# Схема для создания тега
class TagCreate(TagBase):
    pass

# Схема для обновления тега
class TagUpdate(TagBase):
    pass

# Схема для чтения тега
class TagRead(TagBase):
    id: int

    class Config:
        orm_mode = True
