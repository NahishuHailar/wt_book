# app/migrations/env.py

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Импортируем настройки и модели
from app.core.config import settings
from app.db.database import Base
from app.models.book import Book, Genre
from app.models.author import Author
from app.models.tag import Tag
from app.models.associations import book_tags, author_tags, book_genres

# Конфигурация alembic
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# Настройки логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Выполняет миграции при передаче соединения"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в онлайн-режиме."""
    connectable = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool,
        future=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
