"""
Button configuration module for common ticket interactions.

This module defines reusable button components for common ticket-related
actions, such as canceling a close ticket operation. Buttons are
represented using the BotButton model for consistency across the bot UI.
"""

import discord

from bot.models.bot_button import BotButton

cancel_close_ticket_btn: BotButton = {
    "label": "Cancel",
    "custom_id": "common#cancel_close_ticket.cancel",
    "style": discord.ButtonStyle.secondary,
    "emoji": "❌",
}
