import asyncio
import os

import asyncpg
import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Creates an event loop that is shared by test scenarios and the application"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture()
async def async_db_connection():
    """Provides an asyncpg connection for database queries in tests."""
    db_name = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    conn = await asyncpg.connect(url)
    try:
        yield conn
    finally:
        await conn.close()
