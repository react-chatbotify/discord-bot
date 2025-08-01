"""
Retrieves health of services.

This stub is created because the python-genai sdk integration with MCP is experimental
and currently supports local MCP servers. Since we're talking to a remote MCP server,
we'll need to parse the response received to ensure it's what Gemini expects. We should
relook at the need for this stub in future when MCP support is more stable in the sdk.

todo: revisit this
"""

from typing import Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config
from bot.utils.console_logger import console_logger

headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}


async def get_service_health(service_name: str) -> Dict:
    """
    If `service_name` is `"all"`, each known service will be queried in
    sequence. Otherwise only the requested service is checked.

    Args:
        service_name (str): The name of the service to check.

    Returns:
        result_dict (Dict): Dictionary containing result e.g. {'gallery-website': {'status': 'ok'}}

    """
    async with streamablehttp_client(command_center_config.mcp_server_url, headers=headers) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            mcp_response = await session.call_tool("get_service_health", arguments={"service_name": service_name})
            console_logger.debug(f"Received raw MCP response object: {mcp_response}")

            result_dict = mcp_response.structuredContent["result"]
            console_logger.debug(f"Extracted result passed to Gemini: {result_dict}")

            return result_dict
