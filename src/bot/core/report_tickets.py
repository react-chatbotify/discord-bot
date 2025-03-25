"""
Report ticket handler module for processing and setting up report tickets.

This module contains logic for creating and managing report tickets
based on user interaction with buttons or slash commands. It includes
functions for handling theme and plugin report types, configuring
permissions, sending ticket info embeds, and setting up the ticket
system in a given channel.
"""

from typing import Union

import discord
from discord.ext import commands

from bot.config.common import common_config
from bot.config.report_tickets import report_tickets_config
from bot.database.mysql.ticket_counter import get_next_ticket_number
from bot.services.discord_svc import (
    create_channel,
    set_member_channel_permissions,
    set_role_channel_permissions,
)
from bot.ui.embeds.report_tickets.main_menu import MainMenuEmbed
from bot.ui.embeds.report_tickets.report_plugin_info import ReportPluginInfoEmbed
from bot.ui.embeds.report_tickets.report_theme_info import ReportThemeInfoEmbed
from bot.utils.console_logger import console_logger


async def on_report_theme(interaction: discord.Interaction):
    """
    Handle the theme report button click.

    Forwards the interaction to the report ticket processor with "theme" type.

    Args:
        interaction (discord.Interaction): The Discord interaction.

    Returns:
        bool: Whether the report ticket was created successfully.

    """
    return await _create_report_ticket(interaction.user, interaction, "theme")


async def on_report_plugin(interaction: discord.Interaction):
    """
    Handle the plugin report button click.

    Forwards the interaction to the report ticket processor with "plugin" type.

    Args:
        interaction (discord.Interaction): The Discord interaction.

    Returns:
        bool: Whether the report ticket was created successfully.

    """
    return await _create_report_ticket(interaction.user, interaction, "plugin")


async def process_report_ticket_command(ctx: commands.Context) -> bool:
    """
    Handle the /create_report_ticket slash command.

    Args:
        ctx (commands.Context): The context of the command.

    Returns:
        bool: Whether the report ticket was created successfully.

    """
    return await _create_report_ticket(ctx.author, ctx)


async def handle_setup_report_tickets_module(ctx: commands.Context, channel: discord.TextChannel):
    """
    Set up the report tickets module in a given channel.

    Sends the main menu embed to the specified channel.

    Args:
        ctx (commands.Context): The command context.
        channel (discord.TextChannel): The channel to set up the system in.

    """
    main_menu_embed = MainMenuEmbed
    await main_menu_embed.send(ctx, channel)


async def _create_report_ticket(
    user: discord.Member,
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
    report_type: str,
) -> bool:
    """
    Create a report ticket channel for the user.

    This function handles both button-triggered and slash-command-triggered ticket creation,
    sets permissions, and sends an appropriate info embed into the new ticket channel.

    Args:
        user (discord.Member): The member creating the ticket.
        ctx_or_interaction (Union[commands.Context, discord.Interaction]): The context or interaction source.
        report_type (str): The type of report ("theme" or "plugin").

    Returns:
        bool: Whether the report ticket channel was created successfully.

    """
    # Generate ticket details
    if isinstance(ctx_or_interaction, commands.Context):
        bot = ctx_or_interaction.bot
    else:
        bot = ctx_or_interaction.client

    ticket_number = await get_next_ticket_number("report_tickets")
    channel_name = f"📌-report-{ticket_number}"

    # Create private channel
    guild = user.guild
    admin_role = guild.get_role(common_config.admin_role_id)
    channel = await create_channel(
        bot,
        ctx_or_interaction,
        channel_name,
        report_tickets_config.report_tickets_category_id,
        private=True,
    )
    if not channel:
        console_logger.error("❌ Failed to create a report ticket channel.")
        return False

    # Add ticket creator to channel
    await set_member_channel_permissions(
        channel,
        member_permissions=[
            {
                "members": user,
                "permissions": {"read_messages": True, "send_messages": True},
            }
        ],
    )

    # Add admins to channel
    await set_role_channel_permissions(
        channel,
        role_permissions=[
            {
                "roles": admin_role,
                "permissions": {"read_messages": True, "send_messages": True},
            }
        ],
    )

    # Send appropriate ticket info embed
    if report_type == "theme":
        report_ticket_info_embed = ReportThemeInfoEmbed
    else:
        report_ticket_info_embed = ReportPluginInfoEmbed

    await report_ticket_info_embed.send(ctx_or_interaction, channel, ticket_number)
    return True
