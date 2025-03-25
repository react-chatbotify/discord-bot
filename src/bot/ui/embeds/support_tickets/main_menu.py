"""
Embed module for the support ticket main menu interface.

This module defines the interactive embed used to initiate support
tickets for eligible sponsors. It provides a brief description of
support tickets to the users.
"""

from typing import Optional

import discord
from discord.ext import commands

from bot.ui.buttons.support_tickets.main_menu import create_ticket_btn
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class MainMenuEmbed:
    """
    Handler for the support ticket main menu embed and interactions.
    """

    @staticmethod
    async def send(
        ctx: commands.Context,
        channel: Optional[discord.TextChannel] = None,
    ):
        """
        Send the support ticket main menu embed to the given channel.

        Args:
            ctx (commands.Context): The context used to invoke the setup.
            channel (Optional[discord.TextChannel]): The channel to send the embed in.
                Defaults to the channel from the context.

        """
        target_channel = channel or ctx.channel
        try:
            await EmbedsManager.send_embed(
                ctx,
                channel=target_channel,
                title="📩 Support Ticket System",
                description=(
                    "Looking to expedite your issue, seeking suggestions, or perhaps another opinion? "
                    "Click the button below to open a premium support ticket!\n\n"
                    "Available for **Bronze, Silver, Gold, and Platinum Sponsors**."
                ),
                color=discord.Color.blue().value,
                footer_text="Support Ticket System",
                buttons=[create_ticket_btn],
            )

            await EmbedsManager.send_embed(
                ctx,
                title="Setup Complete",
                description=f"✅ Support ticket system has been set up in {target_channel.mention}",
                color=discord.Color.green().value,
                ephemeral=True,
            )

        except Exception as e:
            console_logger.error(f"❌ Error sending setup message: {e}")
