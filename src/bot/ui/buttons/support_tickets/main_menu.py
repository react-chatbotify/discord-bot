"""
Button configuration module for creating support tickets.

This module defines the 'Create Ticket' button used in the support
ticket main menu. The button is styled and configured using the
BotButton model to initiate the ticket creation flow for eligible users.
"""

import discord

from bot.models.bot_button import BotButton

create_ticket_btn: BotButton = {
    "label": "Create Ticket",
    "custom_id": "support_tickets#main_menu.create_ticket",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
