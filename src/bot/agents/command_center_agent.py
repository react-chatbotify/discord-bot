"""
Defines the Agent class for interacting with the Google Gemini API and MCP server.
"""

import json

from google import genai
from google.genai.types import GenerateContentConfig
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config
from bot.models.prompt import Prompt
from bot.utils.console_logger import console_logger

SYSTEM_CONTEXT = (
    "You are a helpful assistant that manages react-chatbotify services. "
    "You can help users by providing information about the services, their health status, "
    "and perform troubleshooting steps such as restarting services. These are the names of "
    "the available services: {services}"
)


class CommandCenterAgent:
    """
    The CommandCenterAgent class for interacting with the Google Gemini API and MCP server.
    """

    def __init__(self):
        """
        Initialize the CommandCenterAgent.

        Sets up authentication headers and internal data structures used to manage
        prompt templates retrieved from the MCP server. These include:
        """
        # Holds all user‐role prompt templates for client‐side selection
        self.system_context: str = ""
        self.user_prompts: list[Prompt] = []
        self.headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}
        self.client = genai.Client()

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
                self.system_context = SYSTEM_CONTEXT.replace("{services}", services_string)

                console_logger.info("Final System Context:")
                console_logger.info(self.system_context)

    async def get_agent_response(self, user_request: str) -> tuple[str, list[dict]]:
        """
        Send the user's request to Gemini with automatic function‐calling.

        then returns a tuple of:
          1) the assistant's final text
          2) a list of all actions taken, e.g. [{"name": ..., "args": ...}, {"tool": ..., "result": ...}, ...]
        """
        async with streamablehttp_client(command_center_config.mcp_server_url, headers=self.headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # set up Gemini with auto function‐calling
                chat = self.client.aio.chats.create(
                    model=command_center_config.gemini_model,
                    config=GenerateContentConfig(
                        temperature=0,
                        tools=[session],
                    ),
                )

                # send the user message and await the final assistant reply
                response = await chat.send_message(user_request)

                # now collect every function_call + tool response from the history
                actions: list[dict] = []
                # history = await chat.history_async()
                # for msg in history:
                #     if msg.role == "model" and msg.parts[0].function_call:
                #         function_call = msg.parts[0].function_call
                #         actions.append({"name": function_call.name, "args": dict(function_call.args)})
                #     if msg.role == "tool":
                #         result_text = ""
                #         if isinstance(msg.content, types.TextContent):
                #             result_text = msg.content.text
                #         actions.append({"tool": msg.name, "result": result_text})

                # finally return (assistant_text, actions_list)
                return response.text, actions
