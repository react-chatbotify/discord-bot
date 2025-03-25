"""
Sponsor ticket handler module for processing and setting up sponsor tickets.

This module contains logic for creating and managing sponsor ticket
channels based on user interactions (button presses or slash commands).
It handles setup of private ticket channels, permission assignment, and
sending appropriate information embeds depending on the sponsor-related
action selected.
"""

from typing import Union

import discord
from discord.ext import commands

from bot.config.common import common_config
from bot.config.sponsor_tickets import sponsor_tickets_config
from bot.database.mysql.ticket_counter import get_next_ticket_number
from bot.services.discord_svc import (
    create_channel,
    set_member_channel_permissions,
    set_role_channel_permissions,
)
from bot.ui.embeds.sponsor_tickets.become_sponsor_info import BecomeSponsorInfoEmbed
from bot.ui.embeds.sponsor_tickets.claim_sponsor_role_info import (
    ClaimSponsorRoleInfoEmbed,
)
from bot.ui.embeds.sponsor_tickets.main_menu import MainMenuEmbed
from bot.ui.embeds.sponsor_tickets.submit_enquiry_info import SubmitEnquiryInfoEmbed
from bot.utils.console_logger import console_logger


async def on_become_a_sponsor(interaction: discord.Interaction):
    """
    Handle the 'Become a Sponsor' button interaction.

    Forwards the interaction to the sponsor ticket processor.

    Args:
        interaction (discord.Interaction): The interaction that triggered the event.

    Returns:
        bool: Whether the sponsor ticket was created successfully.

    """
    return await _create_sponsor_ticket(interaction.user, interaction, "become_a_sponsor")


async def on_claim_sponsor_role(interaction: discord.Interaction):
    """
    Handle the 'Claim Sponsor Role' button interaction.

    Forwards the interaction to the sponsor ticket processor.

    Args:
        interaction (discord.Interaction): The interaction that triggered the event.

    Returns:
        bool: Whether the sponsor ticket was created successfully.

    """
    return await _create_sponsor_ticket(interaction.user, interaction, "claim_sponsor_role")


async def on_submit_enquiry(interaction: discord.Interaction):
    """
    Handle the 'Submit Enquiry' button interaction.

    Forwards the interaction to the sponsor ticket processor.

    Args:
        interaction (discord.Interaction): The interaction that triggered the event.

    Returns:
        bool: Whether the sponsor ticket was created successfully.

    """
    return await _create_sponsor_ticket(interaction.user, interaction, "submit_enquiry")


async def process_sponsor_ticket_command(ctx: commands.Context) -> bool:
    """
    Handle the /create_sponsor_ticket slash command.

    Args:
        ctx (commands.Context): The command context.

    Returns:
        bool: Whether the sponsor ticket was created successfully.

    """
    return await _create_sponsor_ticket(ctx.author, ctx)


async def handle_setup_sponsor_tickets_module(ctx: commands.Context, channel: discord.TextChannel):
    """
    Send the sponsor ticket main menu to a specified channel.

    Args:
        ctx (commands.Context): The command context.
        channel (discord.TextChannel): The channel in which to set up the module.

    """
    main_menu_embed = MainMenuEmbed
    await main_menu_embed.send(ctx, channel)


async def _create_sponsor_ticket(
    user: discord.Member,
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
    action: str,
) -> bool:
    """
    Create a sponsor ticket channel for a user.

    Handles creation and setup of a private ticket channel for sponsor-related
    interactions via slash command or button press.

    Args:
        user (discord.Member): The user initiating the ticket.
        ctx_or_interaction (Union[commands.Context, discord.Interaction]): The context or interaction.
        action (str): The action type (e.g., "become_a_sponsor", "claim_sponsor_role", "submit_enquiry").

    Returns:
        bool: True if the channel was created successfully, False otherwise.

    """
    if isinstance(ctx_or_interaction, commands.Context):
        bot = ctx_or_interaction.bot
    else:
        bot = ctx_or_interaction.client

    ticket_number = await get_next_ticket_number("sponsor_tickets")
    channel_name = f"📌-sponsor-{ticket_number}"

    guild = user.guild
    admin_role = guild.get_role(common_config.admin_role_id)

    channel = await create_channel(
        bot,
        ctx_or_interaction,
        channel_name,
        sponsor_tickets_config.sponsor_tickets_category_id,
        private=True,
    )
    if not channel:
        console_logger.error("❌ Failed to create a sponsor ticket channel.")
        return False

    await set_member_channel_permissions(
        channel,
        member_permissions=[
            {
                "members": user,
                "permissions": {"read_messages": True, "send_messages": True},
            }
        ],
    )

    await set_role_channel_permissions(
        channel,
        role_permissions=[
            {
                "roles": admin_role,
                "permissions": {"read_messages": True, "send_messages": True},
            }
        ],
    )

    if action == "become_a_sponsor":
        sponsor_ticket_info_embed = BecomeSponsorInfoEmbed
    elif action == "claim_sponsor_role":
        sponsor_ticket_info_embed = ClaimSponsorRoleInfoEmbed
    else:
        sponsor_ticket_info_embed = SubmitEnquiryInfoEmbed

    await sponsor_ticket_info_embed.send(ctx_or_interaction, channel, ticket_number)
    return True
