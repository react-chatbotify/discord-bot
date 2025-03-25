"""
Button configuration module for report ticket actions.

This module defines buttons used in the report ticket main menu,
allowing users to initiate a report for either a theme or a plugin. Each
button is configured using the BotButton model and styled for clear user
interaction.
"""

import discord

from bot.models.bot_button import BotButton

report_theme_btn: BotButton = {
    "label": "Report a Theme",
    "custom_id": "report_tickets#main_menu.report_a_theme",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
report_plugin_btn: BotButton = {
    "label": "Report a Plugin",
    "custom_id": "report_tickets#main_menu.report_a_plugin",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
