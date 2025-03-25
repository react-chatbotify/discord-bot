"""
Button configuration module for confirming ticket closure.

This module defines the "Confirm" button used in the close ticket
confirmation flow. It leverages the BotButton model and is styled to
indicate a critical action.
"""

import discord

from bot.models.bot_button import BotButton

confirm_close_ticket_btn: BotButton = {
    "label": "Confirm",
    "custom_id": "common#confirm_close_ticket.confirm",
    "style": discord.ButtonStyle.danger,
    "emoji": "✅",
}
