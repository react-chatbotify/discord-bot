"""
Triggers alert to user.
"""

from typing import Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config

headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}


async def trigger_user(message: str) -> Dict:
    """Send an alert message to the monitoring system."""
    async with streamablehttp_client(command_center_config.mcp_server_url, headers=headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                return await session.call_tool("trigger_user", arguments={"message": message})