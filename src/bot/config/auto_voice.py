"""
AutoVoiceConfig module for managing auto voice channel settings.

This module defines configuration settings for the bot's automatic voice
channel system. It uses Pydantic for validation and loading of
environment- based or default values related to the 'Join to Create'
feature.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class AutoVoiceConfig(BaseSettings):
    """
    Configuration settings for the auto voice feature.

    This configuration holds IDs and parameters related to auto-generated
    voice channels used in the bot's auto voice system.

    Attributes:
        auto_voice_channel_id (int): The ID of the 'Join to Create' voice channel.

    """

    auto_voice_channel_id: int = Field(default=0, description="The ID of the 'Join to Create' voice channel.")


auto_voice_config = AutoVoiceConfig()
