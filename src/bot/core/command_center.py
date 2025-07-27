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
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.ui.prompts.prompts_manager import PromptsManager


async def handle_prompt_input(interaction: discord.Interaction) -> Optional[str]:
    """
    Entry point for handling prompt-based interactions via Discord UI components.

    Forwards the message context from a Discord interaction to the message input
    handler, which queries the AI agent and sends a response if needed.

    Args:
        interaction (discord.Interaction): The interaction that triggered the prompt.

    """
    await handle_message_input(interaction.client, interaction.message)


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
        if prompts:
            await PromptsManager.send_prompt(
                channel=message.channel,
                message="Perhaps I can help you with the following:",
                prompts=prompts,
            )
        else:
            await message.channel.send("What would you like me to help you with today?")
        return

    # lets agent handle the request and return a response text along with actions taken
    response_text, actions = await agent.get_agent_response(user_request)

    # log the actions taken by the agent
    if actions:
        action_descriptions = []
        for i, act in enumerate(actions):
            # get the actual result from the action dictionary
            result_text = act.get("result", "No result returned.")

            # truncate the result if it's too long
            if isinstance(result_text, (dict, list)):
                result_text = str(result_text)
            if len(result_text) > 200:
                result_text = result_text[:200] + "..."

            action_log = (
                f"**{i+1}. Tool: `{act.get('name')}`**\n"
                f"- **Args:** `{act.get('args')}`\n"
                f"- **Result:** `{result_text}`\n"
            )
            action_descriptions.append(action_log)

        # send agent actions as an embed for visual clarity
        # todo: add toggle for verbosity?
        await EmbedsManager.send_embed(
            await bot.get_context(message),
            title="⚙️ Agent Actions",
            description="\n".join(action_descriptions),
            color=discord.Color.blue().value,
            persistent=False,
        )

    return response_text
