"""
Embed module for support ticket creation instructions and actions.

This module defines the interactive embed shown after a user opens a
support ticket. It provides a recommended template for submitting issue
details.
"""

import discord

from bot.ui.buttons.common.close_ticket import close_ticket_btn
from bot.ui.buttons.common.export_ticket import export_ticket_btn
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class NewTicketInfoEmbed:
    """
    Embed handler for support ticket creation instructions and interactions.
    """

    @staticmethod
    async def send(
        ctx_or_interaction,
        channel: discord.TextChannel,
        ticket_number: int,
    ) -> bool:
        """
        Send the support ticket instructions and a confirmation embed.

        Args:
            ctx_or_interaction: The command context or interaction that triggered the embed.
            channel (discord.TextChannel): The channel where the embed should be sent.
            ticket_number (int): The assigned ticket number for reference.

        Returns:
            bool: True if the embed was sent successfully, False otherwise.

        """
        try:
            await EmbedsManager.send_embed(
                ctx_or_interaction,
                channel=channel,
                title="🗳 Support Ticket Opened",
                description=(
                    "Hello there! Please describe your issue(s) in as much detail as possible.\n\n"
                    "**🔹 Below is a suggested template:**\n"
                    "1️⃣ **Type of issue** (e.g. bug, clarification required)\n"
                    "2️⃣ **Issue description** (e.g. button does not work)\n"
                    "3️⃣ **Urgency** (e.g. low priority, very urgent)\n\n"
                    "⚠️ **If reaching out for help with a bug, provide steps to reproduce it.**\n\n"
                    "📌 **Note:** Tickets will be addressed as soon as possible.\n"
                    "You will typically get a **first response within 24 hours**, "
                    "but resolution time may vary. Thank you for your understanding!"
                ),
                color=discord.Color.blue().value,
                footer_text=f"Ticket #{ticket_number}",
                buttons=[close_ticket_btn, export_ticket_btn],
            )

            await EmbedsManager.send_embed(
                ctx_or_interaction,
                title="Ticket Created",
                description=f"✅ Support ticket created: {channel.mention}",
                color=discord.Color.green().value,
                ephemeral=True,
            )

            return True

        except Exception as e:
            console_logger.error(f"❌ Error sending message to support channel: {str(e)}")
            return False
