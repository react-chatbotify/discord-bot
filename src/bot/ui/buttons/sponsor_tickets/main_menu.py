"""
Button configuration module for sponsor ticket actions.

This module defines buttons used in the sponsor ticket main menu,
including options for becoming a sponsor, claiming a sponsor role, and
submitting an enquiry. Each button is represented using the BotButton
model.
"""

import discord

from bot.models.bot_button import BotButton

become_a_sponsor_btn: BotButton = {
    "label": "Become a Sponsor",
    "custom_id": "sponsor_tickets#main_menu.become_a_sponsor",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
claim_sponsor_role_btn: BotButton = {
    "label": "Claim Sponsor Role",
    "custom_id": "sponsor_tickets#main_menu.claim_sponsor_role",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
submit_enquiry_btn: BotButton = {
    "label": "Submit Enquiry",
    "custom_id": "sponsor_tickets#main_menu.submit_enquiry",
    "style": discord.ButtonStyle.primary,
    "emoji": "🎫",
}
