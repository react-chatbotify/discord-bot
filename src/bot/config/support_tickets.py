"""
SupportTicketsConfig module for configuring support ticket settings.

This module defines the configuration used to determine where support
tickets are created within the Discord server. It uses Pydantic to
validate and manage the category ID associated with general support
requests.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class SupportTicketsConfig(BaseSettings):
    """
    Configuration settings for support tickets.

    This configuration defines where support tickets should be created.

    Attributes:
        support_tickets_category_id (int): The Discord category ID for support tickets.

    """

    support_tickets_category_id: int = Field(
        default=0,
        description="The Discord category ID where support tickets are created.",
    )


support_tickets_config = SupportTicketsConfig()
