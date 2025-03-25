"""
Database module for managing async SQLAlchemy engine and sessions.

This module configures the asynchronous SQLAlchemy engine and
sessionmaker used by the Discord bot for database operations.
Configuration is loaded via a Pydantic settings model.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from bot.config.database import DatabaseConfig, database_config
from bot.utils.console_logger import console_logger

Base = declarative_base()


class BotDatabase:
    """
    Generalized database handler using SQLAlchemy async ORM.

    This class sets up the async database engine and session factory,
    and provides methods for initializing and closing the database connection.

    Attributes:
        db_config (DatabaseConfig): The database configuration object.
        database_url (str): Full connection URL built from config values.
        engine: The SQLAlchemy async engine instance.
        async_session: The session factory for async sessions.

    """

    def __init__(self, db_config: DatabaseConfig):
        """
        Initialize the database engine and session factory.

        Args:
            db_config (DatabaseConfig): Configuration for the MySQL connection.

        """
        self.db_config = db_config
        self.database_url = (
            f"mysql+aiomysql://{db_config.mysql_user}:{db_config.mysql_password}@"
            f"{db_config.mysql_host}:{db_config.mysql_port}/{db_config.mysql_database}"
        )
        self.engine = create_async_engine(self.database_url, echo=True)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def close(self):
        """
        Dispose of the engine and close all active connections.
        """
        await self.engine.dispose()
        console_logger.info("✅ Database connection closed!")


# Initialize the database using the Pydantic config.
bot_database = BotDatabase(database_config)
