"""
Button configuration module for exporting ticket content.

This module defines the "Export Ticket" button using the BotButton
model. It is used in the ticket interface to allow users to download the
full message history of a support ticket.
"""

import discord

from bot.models.bot_button import BotButton

export_ticket_btn: BotButton = {
    "label": "Export Ticket",
    "custom_id": "common#export_ticket.export_ticket",
    "style": discord.ButtonStyle.secondary,
    "emoji": "📥",
}
