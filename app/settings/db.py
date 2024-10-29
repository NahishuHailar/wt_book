from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


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
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"


# Instantiate settings
settings = Settings()

# Create the database engine with asyncpg
engine = create_async_engine(settings.db_url, echo=settings.db_echo)

# Create a session factory
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# DB handler class for dependency injection in routes
class DBHandler:
    def __init__(self, engine):
        self.engine = engine
        self.session = async_sessionmaker(bind=engine)

    async def get_db(self) -> AsyncSession:
        async with self.session() as session:
            yield session


# Instantiate a handler for database operations
db_handler = DBHandler(engine)
