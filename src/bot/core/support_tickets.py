"""
Support ticket handler module for processing and setting up support tickets.

This module implements logic for managing support tickets created by
recurring sponsors. It supports both slash command and button
interaction flows, creates private ticket channels with tier-specific
naming, configures permissions, and sends relevant informational embeds
to guide users through the support process.
"""

from typing import List, Union

import discord
from discord.ext import commands

from bot.config.common import common_config
from bot.config.support_tickets import support_tickets_config
from bot.database.mysql.ticket_counter import get_next_ticket_number
from bot.models.sponsor_tier import SponsorTier
from bot.services.discord_svc import (
    create_channel,
    set_member_channel_permissions,
    set_role_channel_permissions,
)
from bot.services.role_checker_svc import is_recurring_sponsor_user
from bot.services.user_info_svc import get_user_recurring_sponsor_tiers
from bot.ui.embeds.support_tickets.main_menu import MainMenuEmbed
from bot.ui.embeds.support_tickets.new_ticket_info import NewTicketInfoEmbed
from bot.utils.console_logger import console_logger


async def on_create_ticket(interaction: discord.Interaction):
    """
    Handle the support ticket button interaction.

    Only recurring sponsors can use this. If valid, triggers ticket creation.

    Args:
        interaction (discord.Interaction): The interaction that triggered the event.

    Returns:
        Optional[discord.Message]: A response message or None if handled silently.

    """
    if not is_recurring_sponsor_user(interaction.user):
        return await interaction.response.send_message(
            "🚫 You must be a sponsor to create premium support tickets.",
            ephemeral=True,
        )
    return await _create_support_ticket(interaction.user, interaction)


async def process_support_ticket_command(ctx: commands.Context) -> bool:
    """
    Handle the /create_support_ticket slash command.

    Args:
        ctx (commands.Context): The command context.

    Returns:
        bool: Whether the support ticket was created successfully.

    """
    return await _create_support_ticket(ctx.author, ctx)


async def handle_setup_support_tickets_module(ctx: commands.Context, channel: discord.TextChannel):
    """
    Set up the support tickets module in a given channel.

    Sends the main menu embed to the specified channel.

    Args:
        ctx (commands.Context): The command context.
        channel (discord.TextChannel): The channel to set up the module in.

    """
    main_menu_embed = MainMenuEmbed
    await main_menu_embed.send(ctx, channel)


async def _create_support_ticket(
    user: discord.Member,
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
) -> bool:
    """
    Create a support ticket channel for a recurring sponsor.

    Generates a private ticket channel with tier-based naming, sets permissions,
    and sends the new ticket info embed into the channel.

    Args:
        user (discord.Member): The user creating the ticket.
        ctx_or_interaction (Union[commands.Context, discord.Interaction]): The context or interaction.

    Returns:
        bool: True if the ticket was created successfully, False otherwise.

    """
    if isinstance(ctx_or_interaction, commands.Context):
        bot = ctx_or_interaction.bot
    else:
        bot = ctx_or_interaction.client

    ticket_number = await get_next_ticket_number("support_tickets")
    sponsor_tiers: List[SponsorTier] = get_user_recurring_sponsor_tiers(user)
    top_tier = sponsor_tiers[0]
    channel_name = f"{common_config.recurring_sponsor_tiers[top_tier].emoji}-support-{ticket_number}"

    guild = user.guild
    admin_role = guild.get_role(common_config.admin_role_id)

    channel = await create_channel(
        bot,
        ctx_or_interaction,
        channel_name,
        support_tickets_config.support_tickets_category_id,
        private=True,
    )
    if not channel:
        console_logger.error("❌ Failed to create a support ticket channel.")
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

    await NewTicketInfoEmbed.send(ctx_or_interaction, channel, ticket_number)
    return True
