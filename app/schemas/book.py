from typing import List, Optional
from pydantic import BaseModel

# Базовая схема для чтения/записи общих полей
class BookBase(BaseModel):
    title: str
    price: float
    quantity: int
    discount: Optional[float] = 0.0

# Схема для создания книги
class BookCreate(BookBase):
    author_id: int
    genre_ids: Optional[List[int]] = []  # ID жанров для связи

# Схема для обновления книги
class BookUpdate(BookBase):
    author_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None

# Схема для чтения книги (ответа API)
class BookRead(BookBase):
    id: int
    author_id: int
    genres: List[str]  # Названия жанров

    class Config:
        orm_mode = True
