"""
Embed module for the sponsor ticket main menu interface.

This module defines the interactive embed used to initiate sponsor
tickets for users. It provides a brief description of sponsor tickets
to the users.
"""

from typing import Optional

import discord
from discord.ext import commands

from bot.ui.buttons.sponsor_tickets.main_menu import (
    become_a_sponsor_btn,
    claim_sponsor_role_btn,
    submit_enquiry_btn,
)
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class MainMenuEmbed:
    """
    Handler for the main menu of the Sponsor Ticket system.
    """

    @staticmethod
    async def send(ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        """
        Send the sponsor ticket main menu embed to the given channel.

        Args:
            ctx (commands.Context): The context from which the command was invoked.
            channel (Optional[discord.TextChannel], optional): The target channel to send the embed to.
                Defaults to the channel from the context.

        """
        target_channel = channel or ctx.channel
        try:
            # Send the main sponsor ticket embed
            await EmbedsManager.send_embed(
                ctx,
                channel=target_channel,
                title="📩 Sponsor Ticket System",
                description=(
                    "Looking to become a sponsor, have enquiries about sponsoring or claiming your sponsor role? "
                    "This is the place!\n\n"
                ),
                color=discord.Color.blue().value,
                footer_text="Sponsor Ticket System",
                buttons=[
                    become_a_sponsor_btn,
                    submit_enquiry_btn,
                    claim_sponsor_role_btn,
                ],
            )

            # Send setup confirmation to the user
            await EmbedsManager.send_embed(
                ctx,
                title="Setup Complete",
                description=f"✅ Sponsor ticket system has been set up in {target_channel.mention}",
                color=discord.Color.green().value,
                ephemeral=True,
            )

        except Exception as e:
            console_logger.error(f"❌ Error sending setup message: {e}")
