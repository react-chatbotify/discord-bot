"""
ReportTicketsConfig module for configuring report ticket settings.

This module defines the configuration used to determine where report
tickets are created within the Discord server. It uses Pydantic to load
and validate the category ID for organizing report-related interactions.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class ReportTicketsConfig(BaseSettings):
    """
    Configuration settings for report tickets.

    This configuration defines where report tickets should be created.

    Attributes:
        report_tickets_category_id (int): The Discord category ID for report tickets.

    """

    report_tickets_category_id: int = Field(
        default=0,
        description="The Discord category ID where report tickets are created.",
    )


report_tickets_config = ReportTicketsConfig()
