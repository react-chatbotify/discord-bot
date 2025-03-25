"""
Common handlers such as for close and export actions of various tickets.

This module defines async functions that respond to UI interactions
related to common modules such as closing tickets or exporting channel
contents. These handlers are triggered by Discord component interactions.
"""

import discord

from bot.services.discord_svc import delete_channel, export_channel_contents
from bot.ui.embeds.common.close_ticket_confirmation import CloseTicketConfirmationEmbed


async def on_close_ticket(interaction: discord.Interaction):
    """
    Handle the close ticket button click.

    Sends a confirmation embed when the user clicks the "Close Ticket" button.

    Args:
        interaction (discord.Interaction): The interaction triggered by the button click.

    """
    close_ticket_confirmation_embed = CloseTicketConfirmationEmbed
    await close_ticket_confirmation_embed.send(interaction)


async def on_export_ticket(interaction: discord.Interaction):
    """
    Handle the download ticket button click.

    Exports the contents of the ticket channel and sends it to the user.

    Args:
        interaction (discord.Interaction): The interaction triggered by the button click.

    """
    bot = interaction.client
    await export_channel_contents(bot, interaction.channel_id, interaction.channel_id)


async def on_confirm_close_ticket(interaction: discord.Interaction):
    """
    Handle the confirm button interaction.

    Deletes the ticket channel.

    Args:
        interaction (discord.Interaction): The interaction that triggered the confirm.

    """
    bot = interaction.client
    await delete_channel(bot, interaction.guild, interaction.channel_id)


async def on_cancel_close_ticket(interaction: discord.Interaction):
    """
    Handle the cancel button interaction.

    Deletes the confirmation prompt without closing the channel.

    Args:
        interaction (discord.Interaction): The interaction that triggered the cancel.

    """
    await interaction.response.defer(ephemeral=True)
    await interaction.delete_original_response()
