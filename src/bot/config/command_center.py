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
        mcp_server_url (str, optional): The URL for the MCP server.

    """

    command_center_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where the command center is created.",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash-lite-preview-06-17",
        description="The model name for the Google Gemini service.",
    )
    mcp_server_url: str = Field(
        default="",
        description="The URL for the MCP server.",
    )
    mcp_server_token: str = Field(
        default="",
        description="The token for the MCP server.",
    )


command_center_config = CommandCenterConfig()
