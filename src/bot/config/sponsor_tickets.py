"""
SponsorTicketsConfig module for configuring sponsor ticket settings.

This module defines the configuration used to determine where sponsor
tickets are created in the Discord server. It uses Pydantic to manage
and validate the category ID related to sponsor support interactions.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class SponsorTicketsConfig(BaseSettings):
    """
    Configuration settings for sponsor tickets.

    This configuration defines where sponsor tickets should be created.

    Attributes:
        sponsor_tickets_category_id (int): The Discord category ID for sponsor tickets.

    """

    sponsor_tickets_category_id: int = Field(
        default=0,
        description="The Discord category ID where sponsor tickets are created.",
    )


sponsor_tickets_config = SponsorTicketsConfig()
