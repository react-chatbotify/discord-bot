"""
Retrieves health of services.
"""

from typing import Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config
from bot.utils.console_logger import console_logger
headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}

async def get_service_health(service_name: str) -> Dict:
    async with streamablehttp_client(command_center_config.mcp_server_url, headers=headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                mcp_response = await session.call_tool("get_service_health", arguments={"service_name": service_name})
                console_logger.info(f"DEBUG: Received raw MCP response object: {mcp_response}")

                # 2. Extract the simple dictionary that the Google AI SDK needs
                #    This is the crucial step!
                result_dict = mcp_response.structuredContent['result']
                
                console_logger.info(f"DEBUG: Extracted this dictionary to return to Gemini: {result_dict}")

                # 3. Return ONLY the simple dictionary
                return result_dict