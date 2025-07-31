"""
Defines the Agent class for interacting with the Google Gemini API and MCP server.
"""

import json

import discord
from google.genai.types import Content
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

from bot.agents.instructions import AGENT_INSTRUCTIONS
from bot.agents.tools.get_service_health import get_service_health
from bot.agents.tools.restart_service import restart_service
from bot.agents.tools.trigger_user import trigger_user
from bot.config.command_center import command_center_config
from bot.llm.gemini import Gemini
from bot.models.prompt import Prompt
from bot.utils.console_logger import console_logger


class CommandCenterAgent:
    """
    The CommandCenterAgent class for interacting with the Google Gemini API and MCP server.

    We're currently not using a persistent session - not great, but acceptable for our use case
    where operations are infrequent. Have explored a bit on persistent session but unable to
    get it to work. Facing a similar issue as what is mentioned in this post:
    https://stackoverflow.com/questions/79692462/fastmcp-client-timing-out-while-initializing-the-session

    todo: we should revisit the above further down the road.
    """

    def __init__(self, bot: discord.Client):
        """
        Initialize the CommandCenterAgent.

        Sets up authentication headers and internal data structures used to manage
        prompt templates retrieved from the MCP server. These include:
        """
        # Holds all user‐role prompt templates for client‐side selection
        self.system_context: str = ""
        self.user_prompts: list[Prompt] = []
        self.headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}
        self.llm = Gemini(command_center_config.gemini_model)

    async def load_all_prompts(self):
        """
        Load all prompts from the MCP server.
        """
        console_logger.info("Initializing prompts from MCP server...")
        async with streamablehttp_client(command_center_config.mcp_server_url, headers=self.headers) as (
            read_stream,
            write_stream,
            _,
        ):
            # create session
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # fetch available prompts
                prompts_response = await session.list_prompts()
                console_logger.info(
                    "Available prompts: %s",
                    [p.name for p in prompts_response.prompts],
                )

                # reset any existing prompts
                self.user_prompts = []

                # populate user prompts
                for prompt_def in prompts_response.prompts:
                    result = await session.get_prompt(prompt_def.name)
                    for msg in result.messages:
                        txt = msg.content.text if isinstance(msg.content, types.TextContent) else str(msg.content)
                        self.user_prompts.append(
                            Prompt(
                                custom_id=prompt_def.name,
                                title=prompt_def.name,
                                description=prompt_def.description[:100],
                                content=txt or "",
                            )
                        )

    async def set_system_context(self):
        """
        Set system context after fetching list of services from the MCP server.
        """
        console_logger.info("Initializing resources from MCP server...")
        async with streamablehttp_client(command_center_config.mcp_server_url, headers=self.headers) as (
            read_stream,
            write_stream,
            _,
        ):
            # create session
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.read_resource("system://services")

                # Extract and parse the JSON text
                services_json = json.loads(result.contents[0].text)
                services_list = services_json["services"]

                # Join services into a comma-separated string
                services_string = ", ".join(services_list)

                # Replace in SYSTEM_CONTEXT
                self.system_context = AGENT_INSTRUCTIONS["system_context"].replace("{services}", services_string)

                console_logger.info("Final System Context:")
                console_logger.info(self.system_context)

    def get_available_tools(self) -> list[str]:
        """
        Get the available tools.

        Returns:
            list[str]: A list of the available tools.
        """
        return [get_service_health.__name__, restart_service.__name__, trigger_user.__name__]

    async def get_agent_response(self, user_input: str, thread: discord.Thread) -> tuple[str, list[dict]]:
        """
        Send the user's request to Gemini with automatic function‐calling.

        Args:
            user_input (str): The user input to the agent.
            thread (discord.Thread): The thread where the conversation is happening.

        Returns:
            tuple[str, list[dict]]: A tuple of:
                1) the assistant's final text
                2) a list of all actions taken, e.g. [{"name": ..., "args": ...}, {"tool": ..., "result": ...}, ...]

        """
        history = await self._get_thread_history(thread)
        tools = [get_service_health, restart_service, trigger_user]

        try:
            response = await self.llm.generate_text(
                user_input, history=history, tools=tools, system_instruction=self.system_context
            )
        except Exception as e:
            console_logger.error(f"An error occurred with the Gemini API: {e}")
            error_message = "I'm sorry, but I encountered a problem while processing your request. Please try again in a moment."
            return error_message, []

        actions = self._extract_actions_from_history(response.history)
        return response.text, actions

    async def _get_thread_history(self, thread: discord.Thread) -> list[dict]:
        """
        Fetch and format the message history from a discord thread.

        Args:
            thread: The thread to get history for.

        Returns:
            list[dict]: A list of dictionaries representing the message history.

        """
        history = []
        async for msg in thread.history(limit=command_center_config.agent_history_size):
            if msg.content.strip() == "":
                continue
            role = "user" if msg.author.id != thread.me.id else "model"
            history.append({"role": role, "parts": [{"text": msg.content}]})

        # reverse the history to have the oldest message first
        history.reverse()
        return history

    def _extract_actions_from_history(self, history: list[Content]) -> list[dict]:
        """
        Parse the chat history to extract all function calls and their results.

        Args:
            history: The conversation history from the Gemini chat session.

        Returns:
            A list of dictionaries, where each dictionary represents an action taken.

        """
        actions: list[dict] = []
        for i, msg in enumerate(history):
            # a function call is initiated by the 'model', and the results are in the next message
            if msg.role == "model" and msg.parts and (i + 1) < len(history):
                next_msg = history[i + 1]

                # ensure the next message is the tool response, which has a 'user' role
                if next_msg.role == "user" and next_msg.parts:

                    # extract function calls, skip any parts that don't contain a valid function_call object
                    function_calls = [part.function_call for part in msg.parts if part.function_call]

                    # extract function responses, skip any parts that don't contain a valid function_response object
                    function_responses = [part.function_response for part in next_msg.parts if part.function_response]

                    # pair up the calls and responses
                    for call, response_part in zip(function_calls, function_responses):
                        if call.name == response_part.name:
                            action = {
                                "name": call.name,
                                "args": dict(call.args),
                                "result": response_part.response,
                            }
                            actions.append(action)
        return actions
