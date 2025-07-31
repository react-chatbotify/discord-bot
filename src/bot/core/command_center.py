"""
Core module for handling Command Center interactions with the Google Gemini API and MCP server.

This module manages the lifecycle of an aiohttp session and defines
logic for communicating with the external SmartChat API. It includes
functions to start and close sessions and retrieve AI-generated
responses based on user input.
"""

from datetime import datetime, timezone
from typing import Optional

import discord
from discord.ext import commands

from bot.agents.agent_manager import AgentManager
from bot.ui.prompts.prompts_manager import PROMPT_ID_TO_TEXT_MAPPING, PromptsManager


async def handle_prompt_input(interaction: discord.Interaction, custom_id: str) -> Optional[str]:
    """
    Entry point for handling prompt-based interactions via Discord UI components.

    Forwards the message context from a Discord interaction to the message input
    handler, which queries the AI agent and sends a response if needed.

    Args:
        interaction (discord.Interaction): The interaction that triggered the prompt.
        custom_id: id of the prompt for mapping to text

    """
    # overwrite the message content with the mapping (default content is just the prompt question)
    interaction.message.content = PROMPT_ID_TO_TEXT_MAPPING[custom_id]

    agents_cog = interaction.client.get_cog("AgentsCog")
    if not agents_cog:
        return

    await handle_message_input(agents_cog.agent_manager, interaction.message)


async def handle_message_input(agent_manager: AgentManager, message: discord.Message):
    """
    Get an AI-generated response for the given message content.

    Sends a request to the SmartChat API with the user's message and returns
    the generated response if applicable.

    Args:
        agent_manager (AgentManager): The agent manager instance.
        message (discord.Message): The message input provided.

    """
    user_request = message.content.replace(f"<@{agent_manager.bot.user.id}>", "").strip()

    # handles the case where the user just mentions the bot without any additional text
    # we'll also only prompt if this is happening inside the main command center channel
    if not user_request and not isinstance(message.channel, discord.Thread):
        async with message.channel.typing():
            prompts = agent_manager.command_center_agent.user_prompts
            if prompts:
                await PromptsManager.send_prompt(
                    channel=message.channel,
                    message="Perhaps I can help you with the following:",
                    prompts=prompts,
                )
            else:
                await message.channel.send("What would you like me to help you with today?")
            return

    thread = message.channel if isinstance(message.channel, discord.Thread) else None
    if not thread:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
        thread_name = f"🤖-{timestamp}"
        thread = await message.create_thread(name=thread_name)

    async with thread.typing():
        await agent_manager.handle_user_message(message.content, thread)
