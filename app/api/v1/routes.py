from fastapi import APIRouter
from app.api.v1.endpoints import authors, books, tags

# Define the main API router with version prefix
v1_router = APIRouter(prefix="/v1")

# Include routers for different resources
v1_router.include_router(authors.router, prefix="/authors", tags=["Authors"])
v1_router.include_router(books.router, prefix="/books", tags=["Books"])
v1_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
