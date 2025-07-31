"""
CommandCenterCog module for handling critical events and interacting with the MCP server.

This module defines a Discord bot cog that provides administrators with an interface
to communicate with Google Gemini, which in turn has access to a remote MCP
(Model Context Protocol) server.
"""

import discord
from discord.ext import commands

from bot.config.command_center import command_center_config
from bot.core.command_center import handle_message_input


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

        agents_cog = self.bot.get_cog("AgentsCog")
        if not agents_cog:
            return

        await handle_message_input(agents_cog.agent_manager, message)


async def setup(bot: commands._Bot):
    """
    Set up the CommandCenterCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(CommandCenter(bot))
