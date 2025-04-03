import logging
from contextlib import asynccontextmanager
from typing import Type, Mapping, Any

import asyncpg
from asyncpg.connection import Connection
from .types import T
from .. import config
from ..observability import with_database_call_measurement

logger = logging.getLogger()


class ConnectionProvider:
    __INSTANCE = None

    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    @classmethod
    async def create(cls):
        if ConnectionProvider.__INSTANCE is None:
            logger.info("Creating new connection pool")
            connection_pool = await asyncpg.create_pool(
                min_size=1,
                max_size=100,
                max_inactive_connection_lifetime=30,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                database=config.POSTGRES_DB
            )
            logger.info("Create connection finished")
            provider = cls(connection_pool)
            ConnectionProvider.__INSTANCE = provider
            logger.info("Created new connection pool")

        return ConnectionProvider.__INSTANCE

    @asynccontextmanager
    async def connection(self) -> asyncpg.connection.Connection:
        async with self._connection_pool.acquire() as connection:
            logger.info("Creating new database connection")
            async with connection.transaction():
                yield connection


class DbOperations:

    @staticmethod
    async def insert_record(table_model: Type[T], db_connection: Connection, record: Mapping[str, Any]) -> T:
        """
        Inserts record values into the table model and returns an instance of the table_model
        :param table_model: The table model to return
        :param db_connection: The database connection
        :param record: The table pair of column/value mappings
        :return: The table model representing the inserted record
        """
        values = record.values()
        logger.info("New database record request", extra={"table": table_model.table_name()})

        # create parameters for postgresql, as they start with $
        fields = record.keys()
        params = ", ".join(f"${i + 1}" for i in range(len(fields)))
        columns = ", ".join(fields)

        query = f"""
            INSERT INTO {table_model.table_name()} ({columns})
            VALUES ({params})
            RETURNING {",".join(table_model.model_fields.keys())}
        """
        coro = db_connection.fetchrow(query, *values)
        row = await with_database_call_measurement(query, coro, values)
        logger.info("Created new database record", extra={"table": table_model.table_name()})
        return table_model(**dict(row))

    @staticmethod
    async def get_records(db_connection: Connection):
        """
        """
        query = f"""
            SELECT * from insurance_quote
        """
        coro = db_connection.fetch(query)
        rows = await with_database_call_measurement(query, coro)
        logger.info("Returning records %s", rows)

        return rows
