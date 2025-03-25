"""
Embed module for ticket close confirmation interactions.

This module defines the embed view and interaction logic for confirming
ticket closure. It sends an ephemeral confirmation prompt, and deletes
the message after a short timeout if no action is taken.
"""

import asyncio

import discord

from bot.ui.buttons.common.cancel_close_ticket import cancel_close_ticket_btn
from bot.ui.buttons.common.confirm_close_ticket import confirm_close_ticket_btn
from bot.ui.embeds.embeds_manager import EmbedsManager
from bot.utils.console_logger import console_logger


class CloseTicketConfirmationEmbed:
    """
    Embed handler for displaying a ticket close confirmation prompt.
    """

    @staticmethod
    async def send(interaction: discord.Interaction) -> bool:
        """
        Send the close ticket confirmation embed with buttons and timeout.

        Args:
            interaction (discord.Interaction): The interaction that triggered the confirmation.

        Returns:
            bool: True if sent successfully, False if an error occurred.

        """
        try:
            await EmbedsManager.send_embed(
                interaction,
                title="Close Ticket Confirmation",
                description=(
                    "Are you sure you want to close this ticket? This will **delete the entire channel**. "
                    "If you need a copy of the ticket contents, click on the **Export Ticket** button."
                ),
                color=discord.Color.yellow().value,
                buttons=[confirm_close_ticket_btn, cancel_close_ticket_btn],
                ephemeral=True,
                persistent=False,
            )

            # Delete the message after 10 seconds if no action is taken
            asyncio.create_task(_delete_after_timeout(interaction, 10))

            return True
        except Exception as e:
            console_logger.error(f"❌ Error sending close confirmation: {str(e)}")
            return False


async def _delete_after_timeout(interaction: discord.Interaction, seconds: int):
    """
    Delete the ephemeral confirmation message after a timeout.

    Args:
        interaction (discord.Interaction): The original interaction.
        seconds (int): Time in seconds before deletion.

    """
    await asyncio.sleep(seconds)
    try:
        await interaction.delete_original_response()
    except Exception:
        # The message may already be deleted
        pass
