"""
Database initialization module for creating tables.

This module is responsible for initializing all SQLAlchemy models
registered under the shared Base metadata. It is used during
application startup to ensure required tables are created in the
database before usage.
"""

from bot.database.mysql.bot_database import Base, bot_database
from bot.database.mysql.ticket_counter import TicketCounter
from bot.utils.console_logger import console_logger


async def init_db():
    """
    Initialize the database by creating all registered tables.

    This function connects to the database using the configured async
    engine, runs `Base.metadata.create_all()` to create any missing
    tables, and logs confirmation that the TicketCounter table is
    loaded.
    """
    async with bot_database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    console_logger.info(f"{TicketCounter} table loaded.")
