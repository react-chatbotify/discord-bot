"""
Ticket counter module for tracking and generating unique ticket numbers.

This module defines a SQLAlchemy model for the `ticket_counters` table and
provides async functions to initialize default counters and retrieve the next
ticket number for various ticket types (e.g., support, report, sponsor).
"""

from sqlalchemy import Column, Integer, String, select

from bot.database.mysql.bot_database import Base, bot_database
from bot.utils.console_logger import console_logger


class TicketCounter(Base):
    """
    SQLAlchemy model representing a ticket counter.

    This table tracks incremental ticket numbers by ticket type.

    Attributes:
        counter_type (str): The type of ticket (e.g., 'support_tickets').
        current_count (int): The current ticket number for this type.

    """

    __tablename__ = "ticket_counters"

    counter_type = Column(String(50), primary_key=True)
    current_count = Column(Integer, nullable=False)


async def initialize_ticket_counter_table():
    """
    Initialize the ticket_counters table with default entries.

    Ensures the table exists and adds default counters for:
    - support_tickets
    - report_tickets
    - sponsor_tickets
    """
    async with bot_database.async_session() as session:
        async with session.begin():
            for ticket_type in ["support_tickets", "report_tickets", "sponsor_tickets"]:
                result = await session.execute(select(TicketCounter).where(TicketCounter.counter_type == ticket_type))
                counter = result.scalars().first()
                if not counter:
                    new_counter = TicketCounter(counter_type=ticket_type, current_count=0)
                    session.add(new_counter)
    console_logger.info("✅ Ticket counter database initialized!")


async def get_next_ticket_number(ticket_type: str) -> int:
    """
    Fetch and increment the next ticket number for a given ticket type.

    If no counter exists for the type, one is created starting at 1.

    Args:
        ticket_type (str): The type of ticket (e.g., 'support_tickets').

    Returns:
        int: The next ticket number for the given type.

    """
    async with bot_database.async_session() as session:
        async with session.begin():
            result = await session.execute(select(TicketCounter).where(TicketCounter.counter_type == ticket_type))
            counter = result.scalars().first()
            if not counter:
                counter = TicketCounter(counter_type=ticket_type, current_count=1)
                session.add(counter)
                next_value = 1
            else:
                counter.current_count += 1
                next_value = counter.current_count
    return next_value
