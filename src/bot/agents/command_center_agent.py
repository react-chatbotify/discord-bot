"""
Defines the Agent class for interacting with the Google Gemini API and MCP server.
"""

import google.generativeai as genai
from mcp import ClientSession

from bot.config.command_center import command_center_config
from bot.core.command_center import get_mcp_client


class CommandCenterAgent:
    """
    The CommandCenterAgent class for interacting with the Google Gemini API and MCP server.
    """

    def __init__(self):
        """
        Initialize the CommandCenterAgent.
        """
        self.session = None

    async def __aenter__(self):
        """
        Asynchronous context manager entry.

        Returns:
            (Agent): The agent instance.

        """
        read, write = await get_mcp_client().__aenter__()
        self.session = ClientSession(read, write)
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit.

        Args:
            exc_type (type): The exception type.
            exc_val (Exception): The exception value.
            exc_tb (traceback): The traceback.

        """
        await self.session.close()
        await get_mcp_client().__aexit__(exc_type, exc_val, exc_tb)

    async def get_ai_response(self, user_request: str):
        """
        Generate an AI response using the Google Gemini API and execute tool calls via the MCP server.

        Args:
            user_request (str): The user's request to be processed by the AI.

        Returns:
            (tuple[str, list[str]]): A tuple containing the AI-generated response and a list of tool calls.

        """
        model = genai.GenerativeModel("gemini-1.5-flash", tools=[self.session])
        chat = model.start_chat()
        response = await chat.send_message_async(user_request)

        tool_calls = []
        tool_call_count = 0
        while response.tool_calls and tool_call_count < command_center_config.max_tool_calls:
            for tool_call in response.tool_calls:
                tool_calls.append(f"Tool call: {tool_call.function_call.name} with args {tool_call.function_call.args}")

            response = await chat.send_message_async(response.tool_calls)
            tool_call_count += 1

        if tool_call_count >= command_center_config.max_tool_calls:
            return (
                "Maximum tool calls reached. Could not complete the action.",
                tool_calls,
            )

        return response.text, tool_calls
