"""
Core module for handling Command Center interactions with the Google Gemini API and MCP server.

This module provides functionalities to initialize a connection with the MCP server,
generate AI responses using Google Gemini, and manage the lifecycle of the MCP client session.
"""

import google.generativeai as genai
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
