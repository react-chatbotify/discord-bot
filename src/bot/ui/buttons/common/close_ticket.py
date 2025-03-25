"""
Button configuration module for closing support tickets.

This module defines the "Close Ticket" button using the BotButton model.
It is used in ticket interfaces to allow users to initiate the ticket
closure process via Discord UI components.
"""

import discord

from bot.models.bot_button import BotButton

close_ticket_btn: BotButton = {
    "label": "Close Ticket",
    "custom_id": "common#close_ticket.close_ticket",
    "style": discord.ButtonStyle.danger,
    "emoji": "🔒",
}
