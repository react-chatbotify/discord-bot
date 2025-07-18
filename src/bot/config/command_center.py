"""
CommandCenterConfig module for configuring command center settings.

This module defines the configuration used to determine where the command
center is created within the Discord server. It uses Pydantic to
validate and manage the channel ID associated with the command center.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class CommandCenterConfig(BaseSettings):
    """
    Configuration settings for the command center.

    This configuration defines where the command center should be created
    within the Discord server.

    Attributes:
        command_center_channel_id (int): The Discord channel ID for the command center.

    """

    command_center_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where the command center is created.",
    )


command_center_config = CommandCenterConfig()
