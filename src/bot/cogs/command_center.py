"""
CommandCenterCog module for handling critical events (such as service issues).

This module defines a Discord bot cog that listens for external webhook
events dispatched internally within the bot (e.g., from a local or remote
web server). When a webhook event is received, the cog forwards the message
to a configured channel for alerting and further handling.

The configuration for the destination channel is loaded from the centralized
command center config module.
"""

from discord.ext import commands

from bot.config.command_center import command_center_config


class CommandCenter(commands.Cog):
    """
    A Discord bot cog for processing and routing command center events.

    This cog listens for internally dispatched command center events (e.g.,
    `bot.dispatch("service_issue_event", data)`) and forwards the relevant
    information to a preconfigured channel defined in the command center config.

    Listeners:
        on_service_issue_event:
            - Triggered when an external webhook event is received by the bot.
              Forwards the message to the configured channel.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the CommandCenterCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_service_issue_event(self, data: dict):
        """
        Handle an external webhook event dispatched by the bot to indicate service issue.

        This event listener is triggered when the bot receives a webhook
        event through an internal dispatch (e.g., from an aiohttp server).
        If a channel is configured via `command_center_config`, the event message
        is sent there.

        Args:
            data (dict): The event payload containing at least a 'message' field.

        """
        channel_id = command_center_config.command_center_channel_id
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                message = data.get("message", "No message provided.")
                await channel.send(f"Webhook event received: {message}")


async def setup(bot: commands.Bot):
    """
    Set up the CommandCenterCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(CommandCenter(bot))
