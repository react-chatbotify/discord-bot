"""
Embed module for the report ticket main menu interface.

This module defines the interactive embed used to initiate report
tickets for plugins or themes. It provides a brief description of
report tickets to the users.
"""

from typing import Optional

import discord
from discord.ext import commands

from bot.ui.buttons.report_tickets.main_menu import report_plugin_btn, report_theme_btn
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class MainMenuEmbed:
    """
    Handler for the report ticket main menu embed and its interactions.
    """

    @staticmethod
    async def send(ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        """
        Send the report ticket main menu embed to the given channel.

        Args:
            ctx (commands.Context): The context from which the command was invoked.
            channel (Optional[discord.TextChannel], optional): Target channel to send the embed to.
                Defaults to the channel where the command was used.

        """
        target_channel = channel or ctx.channel
        try:
            # Send the main report ticket embed
            await EmbedsManager.send_embed(
                ctx,
                channel=target_channel,
                title="📩 Report Ticket System",
                description=(
                    "Spotted a malicious plugin, or perhaps an offensive theme? "
                    "Help inform us by creating a report!\n\n"
                    "Note that this is **not for bug reports**."
                ),
                color=discord.Color.blue().value,
                footer_text="Report Ticket System",
                buttons=[report_theme_btn, report_plugin_btn],
            )

            # Notify user of successful setup
            await EmbedsManager.send_embed(
                ctx,
                title="Setup Complete",
                description=f"✅ Report ticket system has been set up in {target_channel.mention}",
                color=discord.Color.green().value,
                ephemeral=True,
            )

        except Exception as e:
            console_logger.error(f"❌ Error sending setup message: {e}")
