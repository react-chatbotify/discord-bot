"""
ReportTicketsCog module for handling Discord report ticket functionality.

This module defines a cog that allows users with appropriate permissions
to create report tickets and lets administrators configure the ticketing
system within a specified text channel. It integrates embed templates
and backend processing for a structured reporting workflow.
"""

import discord
from discord.ext import commands

from bot.button_loaders.report_tickets import ReportTicketsButtonLoader
from bot.core.report_tickets import (
    handle_setup_report_tickets_module,
    process_report_ticket_command,
)
from bot.utils.decorators import admin_only


class ReportTicketsCog(commands.Cog):
    """
    A Discord bot cog for managing report tickets.

    This cog provides commands for opening report tickets (restricted to
    sponsors and admins) and setting up the report ticket system in a
    specified channel.

    Commands:
        /create_report_ticket:
            - Creates a new report ticket (Restricted to sponsors and admins).

        /setup_report_tickets_cog:
            - Configures the report ticket system in a specified channel (Admin only).
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the ReportTicketsCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        ReportTicketsButtonLoader.load_buttons()

    def cog_unload(self):
        """
        Unload the cog and release embedded resources.
        """
        ReportTicketsButtonLoader.unload_buttons()

    @commands.guild_only()
    @commands.hybrid_command(
        name="create_report_ticket",
        description="Open a report ticket",
        with_app_command=True,
    )
    async def create_report_ticket(self, ctx: commands.Context):
        """
        Open a new report ticket.

        This command allows users (with proper permissions) to open a report
        ticket for support or moderation assistance.

        Args:
            ctx (commands.Context): The command context.

        """
        await process_report_ticket_command(ctx)

    @admin_only()
    @commands.guild_only()
    @commands.hybrid_command(
        name="setup_report_tickets_module",
        description="Set up the report ticket system (Admin Only)",
        with_app_command=True,
    )
    async def setup_report_tickets_module(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """
        Configure the report ticket system in the specified channel.

        This admin-only command sets up the report ticket system UI in a
        given text channel. If no channel is specified, the current channel is used.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel, optional): The channel to set up the system in.

        """
        await handle_setup_report_tickets_module(ctx, channel or ctx.channel)


async def setup(bot: commands.Bot):
    """
    Set up the ReportTicketsCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(ReportTicketsCog(bot))
