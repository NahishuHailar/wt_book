import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_book_with_author_and_tag():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создаём автора
        author_response = await ac.post(
            "/v1/authors/",
            json={"name": "Author Test", "country": "Test Country"},
        )
        author_id = author_response.json()["id"]

        # Создаём тег
        tag_response = await ac.post(
            "/v1/tags/", json={"name": "Science Fiction"}
        )
        tag_id = tag_response.json()["id"]

        # Создаём книгу с указанным автором и тегом
        book_response = await ac.post(
            "/v1/books/",
            json={
                "title": "Book with Author and Tag",
                "published_year": 2021,
                "author_id": author_id,
                "tags": [tag_id],
            },
        )

        assert book_response.status_code == 201
        assert book_response.json()["title"] == "Book with Author and Tag"
        assert book_response.json()["author_id"] == author_id
