import asyncio
import logging.config
import os

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

logging.config.fileConfig("alembic.ini")
# Load database URL from alembic.ini

def database_url():
    db_name = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

    return url


config = context.config
DB_URL = database_url()


# Use asyncpg engine
def get_async_engine():
    return create_async_engine(DB_URL,
                               poolclass=pool.NullPool,
                               )


async def run_migrations_online():
    print("running migrations online")

    """Run migrations in 'online' mode with async engine."""
    connectable = get_async_engine()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()


asyncio.run(run_migrations_online())
