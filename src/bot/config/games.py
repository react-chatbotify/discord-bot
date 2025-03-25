"""
GamesConfig module for configuring interactive game channels.

This module defines the configuration for game-related features in the
bot, specifically the Discord channel IDs used for the counting and
story games. Pydantic is used to manage and validate these settings.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class GamesConfig(BaseSettings):
    """
    Configuration settings for interactive games.

    These settings define the Discord channel IDs used for specific game features.

    Attributes:
        count_channel_id (int): The channel ID for the counting game.
        story_channel_id (int): The channel ID for the story game.

    """

    count_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where the counting game takes place.",
    )
    story_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where the story game takes place.",
    )


games_config = GamesConfig()
