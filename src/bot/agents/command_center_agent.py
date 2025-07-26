"""
Defines the Agent class for interacting with the Google Gemini API and MCP server.
"""

from google import genai
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

from bot.config.command_center import command_center_config
from bot.models.prompt import Prompt
from bot.utils.console_logger import console_logger


class CommandCenterAgent:
    """
    The CommandCenterAgent class for interacting with the Google Gemini API and MCP server.
    """

    def __init__(self):
        """
        Initialize the CommandCenterAgent.

        Sets up authentication headers and internal data structures used to manage
        prompt templates retrieved from the MCP server. These include:

        Args:
            system_prompt: A list of system-level prompts used to configure the AI's behavior.
            user_prompts: A list of user-facing prompts that can be selected or presented in the UI.

        """
        # Holds the single system‐role prompt text
        self.system_prompt: list[Prompt] = []
        # Holds all user‐role prompt templates for client‐side selection
        self.user_prompts: list[Prompt] = []
        self.headers = {"Authorization": f"Bearer {command_center_config.mcp_server_token}"}
        self.client = genai.Client()

    async def initialize_prompts(self):
        """
        Fetch prompts from the MCP server.

        System‐role prompts (no required args) populate self.system_prompt.
        User‐role prompts (have required args) populate self.user_prompts and are returned.
        """
        console_logger.info("Initializing prompts from MCP server...")
        async with streamablehttp_client(command_center_config.mcp_server_url, headers=self.headers) as (
            read_stream,
            write_stream,
            _,
        ):
            # create session
            async with ClientSession(read_stream, write_stream) as session:
                # initialize the connection
                console_logger.info(f"Connecting to MCP server at {command_center_config.mcp_server_url}")
                await session.initialize()

                # fetch available prompts
                prompts_response = await session.list_prompts()
                console_logger.info(
                    "Available prompts: %s",
                    [p.name for p in prompts_response.prompts],
                )

                # reset any existing prompts
                self.system_prompt = []
                self.user_prompts = []

                # classify each prompt template
                for prompt_def in prompts_response.prompts:
                    result = await session.get_prompt(prompt_def.name)
                    # look for the first "system" message
                    for msg in result.messages:
                        txt = msg.content.text if isinstance(msg.content, types.TextContent) else str(msg.content)
                        if prompt_def.name.startswith("system://"):
                            self.system_prompt.append(
                                Prompt(
                                    custom_id=prompt_def.name,
                                    title=prompt_def.name,
                                    description=prompt_def.description,
                                    content=txt or "",
                                )
                            )
                            break
                        else:
                            self.user_prompts.append(
                                Prompt(
                                    custom_id=prompt_def.name,
                                    title=prompt_def.name,
                                    description=prompt_def.description[:100],
                                    content=txt or "",
                                )
                            )

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
                    config=genai.types.GenerateContentConfig(
                        temperature=0,
                        tools=[session],
                    ),
                )

                # seed the system prompt if you have one
                if self.system_prompt:
                    await chat.send_message(self.system_prompt[0].content)

                # send the user message and await the final assistant reply
                response = await chat.send_message(user_request)

                # now collect every function_call + tool response from the history
                actions: list[dict] = []
                for msg in chat.history:
                    if msg.role == "model" and msg.parts[0].function_call:
                        function_call = msg.parts[0].function_call
                        actions.append({"name": function_call.name, "args": dict(function_call.args)})
                    if msg.role == "tool":
                        # msg.name is the tool URI/name, msg.content is the body
                        result_text = ""
                        if isinstance(msg.content, types.TextContent):
                            result_text = msg.content.text
                        actions.append({"tool": msg.name, "result": result_text})

                # finally return (assistant_text, actions_list)
                return response.text, actions
