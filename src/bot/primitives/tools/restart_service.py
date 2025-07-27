"""
Restarts services.
"""

from typing import Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config

headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}

async def restart_service(service_name: str, branch: str) -> Dict:
    """Restart the specified service by dispatching a GitHub Actions workflow."""
    async with streamablehttp_client(command_center_config.mcp_server_url, headers=headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                return await session.call_tool("restart_service", arguments={"service_name": service_name})