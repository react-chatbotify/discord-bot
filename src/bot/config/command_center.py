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
        gemini_api_key (str): The API key for the Google Gemini service.
        mcp_server_url (str, optional): The URL for the MCP server.
    """

    command_center_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where the command center is created.",
    )
    gemini_api_key: str = Field(
        default="",
        description="The API key for the Google Gemini service.",
    )
    mcp_server_url: str = Field(
        default="",
        description="The URL for the MCP server.",
    )
    max_tool_calls: int = Field(
        default=10,
        description="The maximum number of tool calls that can be made in a single request.",
    )


command_center_config = CommandCenterConfig()
