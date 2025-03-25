"""
Embed module for plugin report ticket instructions and actions.

This module defines the interactive embed used in plugin-related report
tickets. It sends instructional content to the user, and provides
confirmation messaging upon ticket creation.
"""

import discord

from bot.ui.buttons.common.close_ticket import close_ticket_btn
from bot.ui.buttons.common.export_ticket import export_ticket_btn
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class ReportPluginInfoEmbed:
    """
    Embed handler for plugin report ticket instructions and interactions.
    """

    @staticmethod
    async def send(
        ctx_or_interaction,
        channel: discord.TextChannel,
        ticket_number: int,
    ) -> bool:
        """
        Send the plugin report instructions and a confirmation message.

        Args:
            ctx_or_interaction: The command context or interaction.
            channel (discord.TextChannel): The channel to send the embed in.
            ticket_number (int): The ticket number for reference.

        Returns:
            bool: True if the embed was sent successfully, False otherwise.

        """
        try:
            await EmbedsManager.send_embed(
                ctx_or_interaction,
                channel=channel,
                title="📕 Report a Plugin",
                description=(
                    "Hello there! Please describe the plugin that you are reporting.\n\n"
                    "**🔹 Below is a suggested template:**\n"
                    "1️⃣ **Link to plugin**\n"
                    "2️⃣ **Report description** (e.g. the plugin is malicious)\n"
                    "3️⃣ **Urgency** (e.g. low priority, very urgent)\n\n"
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
                description=f"✅ Report ticket (plugin) created: {channel.mention}",
                color=discord.Color.green().value,
                ephemeral=True,
            )

            return True

        except Exception as e:
            console_logger.error(f"❌ Error sending message to report channel: {str(e)}")
            return False
