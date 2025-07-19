"""
Core module for handling Command Center interactions with the Google Gemini API and MCP server.

This module provides functionalities to initialize a connection with the MCP server,
generate AI responses using Google Gemini, and manage the lifecycle of the MCP client session.
"""

import google.generativeai as genai
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.websocket import websocket_client

from bot.config.command_center import command_center_config


def configure_genai():
    """
    Configure the Google Generative AI client with the API key.
    """
    genai.configure(api_key=command_center_config.gemini_api_key)


def get_mcp_client():
    """
    Get the MCP client based on the configuration.

    Returns:
        (Callable): The MCP client.
    """
    if command_center_config.mcp_server_url:
        return websocket_client(command_center_config.mcp_server_url)
    else:
        return stdio_client(
            StdioServerParameters(
                command="python",
                args=["main.py"],
                env=None,
            )
        )


async def get_ai_response(user_request: str):
    """
    Generate an AI response using the Google Gemini API and execute tool calls via the MCP server.

    Args:
        user_request (str): The user's request to be processed by the AI.

    Returns:
        (tuple[str, list[str]]): A tuple containing the AI-generated response and a list of tool calls.
    """
    async with get_mcp_client() as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            model = genai.GenerativeModel("gemini-1.5-flash", tools=[session])
            chat = model.start_chat()
            response = await chat.send_message_async(user_request)

            tool_calls = []
            tool_call_count = 0
            while (
                response.tool_calls
                and tool_call_count < command_center_config.max_tool_calls
            ):
                for tool_call in response.tool_calls:
                    tool_calls.append(
                        f"Tool call: {tool_call.function_call.name} with args {tool_call.function_call.args}"
                    )

                response = await chat.send_message_async(response.tool_calls)
                tool_call_count += 1

            if tool_call_count >= command_center_config.max_tool_calls:
                return (
                    "Maximum tool calls reached. Could not complete the action.",
                    tool_calls,
                )

            return response.text, tool_calls
