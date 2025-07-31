"""
AlertsCog module for handling incoming webhook alerts.

This module defines a Discord bot cog that manages incoming webhook alerts.
"""

from discord.ext import commands

from bot.config.command_center import command_center_config
from bot.core.alerts import handle_webhook_input


class AlertsCog(commands.Cog):
    """
    A cog for processing and routing webhook alerts.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the AlertsCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_webhook_alert_event(self, data: dict):
        """
        Handle an external webhook event dispatched to the bot.

        Args:
            data (dict): The event payload containing at least a 'type' and 'message' field.

        """
        # if not able to even get channel, nothing to do
        channel_id = command_center_config.command_center_channel_id
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
        if not channel:
            return

        agents_cog = self.bot.get_cog("AgentsCog")
        if not agents_cog:
            return

        # handle service down event
        await handle_webhook_input(agents_cog.agent_manager, channel, data)


async def setup(bot: commands.Bot):
    """
    Set up the AlertsCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(AlertsCog(bot))
