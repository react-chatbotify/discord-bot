"""
CommandCenterCog module for handling critical events and interacting with the MCP server.

This module defines a Discord bot cog that provides administrators with an interface
to communicate with Google Gemini, which in turn has access to a remote MCP
(Model Context Protocol) server.
"""

import traceback

import discord
from discord.ext import commands

from bot.agents.command_center_agent import CommandCenterAgent
from bot.config.command_center import command_center_config
from bot.core.command_center import handle_message_input
from bot.prompt_loaders.mcp import McpPromptLoader
from bot.utils.console_logger import console_logger


class CommandCenter(commands.Cog):
    """
    A Discord bot cog for processing and routing command center events
    and interacting with the MCP server.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the CommandCenterCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        self.agent = CommandCenterAgent()
        self._prompts_initialized = False

    def cog_unload(self):
        """
        Unload the cog and release embedded resources.
        """
        McpPromptLoader.unload_prompts(self.agent.user_prompts)
        self.agent = None
        self._prompts_initialized = False

    # todo: need to restrict to admin role?
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Trigger MCP logic when a message is sent in the command center channel and the bot is mentioned.

        Args:
            message (discord.Message): The message that triggered the event.

        """
        # Ignore bot's own messages
        if message.author.bot:
            return

        # Only act in the command center channel or its threads
        if not (
            message.channel.id == int(command_center_config.command_center_channel_id)
            or (
                isinstance(message.channel, discord.Thread)
                and message.channel.parent_id == int(command_center_config.command_center_channel_id)
            )
        ):
            return

        # Only proceed if the bot is mentioned or message is in a command center thread
        if self.bot.user not in message.mentions and not isinstance(message.channel, discord.Thread):
            return

        await handle_message_input(self.bot, message)


async def setup(bot: commands.Bot):
    """
    Set up the CommandCenterCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    cog = CommandCenter(bot)
    await bot.add_cog(cog)  # Add cog first, so it's fully registered

    # Now manually trigger loading of prompts and setting system context
    try:
        await cog.agent.load_all_prompts()
        McpPromptLoader.load_prompts(cog.agent.user_prompts)
        cog._prompts_initialized = True
    except Exception:
        console_logger.error(f"❌ Failed to load prompts:\n{traceback.format_exc()}")

    try:
        await cog.agent.set_system_context()
    except Exception:
        console_logger.error(f"❌ Failed to set system context:\n{traceback.format_exc()}")
