"""
SmartChatConfig module for configuring AI-powered smart chat integration.

This module defines settings for integrating with an external smart chat
API, including the API endpoint and the list of Discord channel IDs
where smart responses should be enabled. Pydantic is used for managing
and validating these configurations.
"""

from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode


class SmartChatConfig(BaseSettings):
    """
    Configuration settings for smart chat.

    This configuration handles integration with the smart chat AI API and
    specifies which channels are enabled for smart responses.

    Attributes:
        smart_chat_api_url (str): The base URL of the smart chat API.
        smart_chat_channel_ids (List[int]): The list of channel ids where smart chat is enabled.

    """

    smart_chat_api_url: str = Field(
        default="",
        description="The URL endpoint for the external smart chat API.",
    )
    smart_chat_channel_ids: Annotated[List[int], NoDecode] = Field(
        default_factory=list,
        description="Comma-separated channel IDs where smart chat is enabled.",
    )

    @field_validator("smart_chat_channel_ids", mode="before")
    @classmethod
    def parse_channel_ids(cls, v):
        """
        Convert a comma-separated string to a list of smart channel ids.

        Args:
            v (str | list): The raw value from the environment or settings.

        Returns:
            list[int]: A list of cleaned smart channel ids.

        """
        if isinstance(v, str):
            return [int(cid.strip()) for cid in v.split(",") if cid.strip().isdigit()]
        return v


smart_chat_config = SmartChatConfig()
