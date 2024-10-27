from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

# Создаем асинхронный движок для взаимодействия с базой данных
engine = create_async_engine(settings.database_url, echo=True)

# Создаем асинхронные сессии для работы с базой
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Функция для получения сессии базы данных
async def get_db():
    async with async_session() as session:
        yield session
