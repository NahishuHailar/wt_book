# app/main.py
from fastapi import FastAPI
from app.api import books, authors, tags, genres
from app.core.config import settings

app = FastAPI()

# Подключаем маршруты
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])

@app.get("/")
async def root():
    return {"message": "Welcome to the WT Bookstore API!"}
