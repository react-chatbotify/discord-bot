"""
SupportTicketsCog module for managing sponsor-based support tickets.

This module defines a Discord bot cog that allows recurring sponsors and
admins to open support tickets, and enables administrators to configure
the ticketing interface in a specific text channel. It integrates embed
loaders and backend logic for structured support request handling.
"""

import discord
from discord.ext import commands

from bot.button_loaders.support_tickets import SupportTicketsButtonLoader
from bot.core.support_tickets import (
    handle_setup_support_tickets_module,
    process_support_ticket_command,
)
from bot.utils.decorators import admin_only, recurring_sponsor_only


class SupportTicketsCog(commands.Cog):
    """
    A Discord bot cog for managing support tickets.

    This cog provides commands for opening support tickets (restricted to
    sponsors and admins) and setting up the support ticket system in a
    specified channel.

    Commands:
        /create_support_ticket:
            - Creates a new support ticket (Restricted to sponsors and admins).

        /setup_support_tickets_cog:
            - Configures the support ticket system in a specified channel (Admin only).
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the SupportTicketsCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        SupportTicketsButtonLoader.load_buttons()

    def cog_unload(self):
        """
        Unload the cog and release embedded resources.
        """
        SupportTicketsButtonLoader.unload_buttons()

    @recurring_sponsor_only()
    @commands.guild_only()
    @commands.hybrid_command(
        name="create_support_ticket",
        description="Open a support ticket (Sponsors only)",
        with_app_command=True,
    )
    async def create_support_ticket(self, ctx: commands.Context):
        """
        Open a new support ticket.

        This command allows recurring sponsors and admins to open a support
        ticket for assistance or inquiries.

        Args:
            ctx (commands.Context): The command context.

        """
        await process_support_ticket_command(ctx)

    @admin_only()
    @commands.guild_only()
    @commands.hybrid_command(
        name="setup_support_tickets_module",
        description="Set up the support ticket system (Admin Only)",
        with_app_command=True,
    )
    async def setup_support_tickets_module(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """
        Configure the support ticket system in the specified channel.

        This admin-only command sets up the support ticket system UI in a
        given text channel. If no channel is specified, the current channel is used.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel, optional): The channel to configure the system in.

        """
        await handle_setup_support_tickets_module(ctx, channel or ctx.channel)


async def setup(bot: commands.Bot):
    """
    Set up the SupportTicketsCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(SupportTicketsCog(bot))
