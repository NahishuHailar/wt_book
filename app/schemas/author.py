from typing import List, Optional
from pydantic import BaseModel

# Базовая схема для автора
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

# Схема для создания автора
class AuthorCreate(AuthorBase):
    pass

# Схема для обновления автора
class AuthorUpdate(AuthorBase):
    pass

# Схема для чтения автора
class AuthorRead(AuthorBase):
    id: int
    books: List[str]  # Список названий книг

    class Config:
        orm_mode = True
