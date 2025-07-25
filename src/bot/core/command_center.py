"""
Core module for handling Command Center interactions with the Google Gemini API and MCP server.

This module manages the lifecycle of an aiohttp session and defines
logic for communicating with the external SmartChat API. It includes
functions to start and close sessions and retrieve AI-generated
responses based on user input.
"""

from typing import Optional

import discord
from discord.ext import commands

from bot.agents.command_center_agent import CommandCenterAgent
from bot.ui.prompts.prompts_manager import PromptsManager
from bot.utils.console_logger import console_logger


async def handle_prompt_input(interaction: discord.Interaction) -> Optional[str]:
    """
    Entry point for handling prompt-based interactions via Discord UI components.

    Forwards the message context from a Discord interaction to the message input
    handler, which queries the AI agent and sends a response if needed.

    Args:
        interaction (discord.Interaction): The interaction that triggered the prompt.

    """
    handle_message_input(interaction.client, interaction.message)


async def handle_message_input(bot: commands.Bot, message: discord.Message) -> Optional[str]:
    """
    Get an AI-generated response for the given message content.

    Sends a request to the SmartChat API with the user's message and returns
    the generated response if applicable.

    Args:
        bot: The Discord bot instance.
        message (discord.Message): The message input provided.

    Returns:
        Optional[str]: The AI-generated response, or None if no response should be sent.

    """
    cog = bot.get_cog("CommandCenter")
    if cog:
        agent: CommandCenterAgent = cog.agent
    user_request = message.content.replace(f"<@{bot.user.id}>", "").strip()

    # handles the case where the user just mentions the bot without any additional text
    if not user_request:
        prompts = agent.user_prompts
        console_logger.info("Checkpoint AAA")
        console_logger.info(f"Available prompts: {prompts}")
        if prompts:
            await PromptsManager.send_prompt(
                channel=message.channel,
                message="Perhaps I can help you with the following:",
                prompts=prompts,
            )
        else:
            console_logger.info("Checkpoint 3")
            await message.channel.send("What would you like me to help you with today?")
        return

    # lets agent handle the request and return a response text along with actions taken
    response_text, actions = await agent.get_agent_response(user_request)

    # log the actions taken by the agent
    for act in actions:
        if act.get("name"):
            # this was a function_call
            await message.channel.send(f"🛠 Called `{act['name']}` with args {act['args']}")
        elif act.get("tool"):
            # this was the tool’s output
            await message.channel.send(f"🔧 Tool `{act['tool']}` returned: {act['result']}")

    return response_text
