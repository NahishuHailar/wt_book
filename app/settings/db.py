from typing import AsyncGenerator

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# Settings class to handle environment variables
class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str
    db_port: str
    db_echo: bool = True

    # URL for connecting to the database
    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


# Instantiate settings
settings = Settings()


# DB handler class for dependency injection in routes
class Database:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def scoped_session_dependency(self) -> AsyncGenerator:
        async with self.session_factory() as session:
            yield session
            await session.close()


# Instantiate a handler for database operations
db_handler = Database(settings.db_url, settings.db_echo)
