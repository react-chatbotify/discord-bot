"""
SponsorTicketsCog module for handling sponsor ticket functionality.

This module defines a Discord bot cog that allows sponsors and admins to
open special support tickets and enables admins to configure the sponsor
ticketing system in a designated channel. It integrates embedded UI
components and backend processing for ticket management.
"""

import discord
from discord.ext import commands

from bot.button_loaders.sponsor_tickets import SponsorTicketsButtonLoader
from bot.core.sponsor_tickets import (
    handle_setup_sponsor_tickets_module,
    process_sponsor_ticket_command,
)
from bot.utils.decorators import admin_only


class SponsorTicketsCog(commands.Cog):
    """
    A Discord bot cog for managing sponsor tickets.

    This cog provides commands for opening sponsor tickets (restricted to
    sponsors and admins) and setting up the sponsor ticket system in a
    specified channel.

    Commands:
        /create_sponsor_ticket:
            - Creates a new sponsor ticket (Restricted to sponsors and admins).

        /setup_sponsor_tickets_cog:
            - Configures the sponsor ticket system in a specified channel (Admin only).
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the SponsorTicketsCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        SponsorTicketsButtonLoader.load_buttons()

    def cog_unload(self):
        """
        Unload the cog and release embedded resources.
        """
        SponsorTicketsButtonLoader.unload_buttons()

    @commands.guild_only()
    @commands.hybrid_command(
        name="create_sponsor_ticket",
        description="Open a sponsor ticket",
        with_app_command=True,
    )
    async def create_sponsor_ticket(self, ctx: commands.Context):
        """
        Open a new sponsor ticket.

        This command allows authorized users to open a sponsor ticket for
        exclusive support or requests.

        Args:
            ctx (commands.Context): The command context.

        """
        await process_sponsor_ticket_command(ctx)

    @admin_only()
    @commands.guild_only()
    @commands.hybrid_command(
        name="setup_sponsor_tickets_module",
        description="Set up the sponsor ticket system (Admin Only)",
        with_app_command=True,
    )
    async def setup_sponsor_tickets_module(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """
        Configure the sponsor ticket system in the specified channel.

        This admin-only command sets up the sponsor ticket system UI in a
        given text channel. If no channel is specified, the current channel is used.

        Args:
            ctx (commands.Context): The command context.
            channel (discord.TextChannel, optional): The channel to configure the system in.

        """
        await handle_setup_sponsor_tickets_module(ctx, channel or ctx.channel)


async def setup(bot: commands.Bot):
    """
    Set up the SponsorTicketsCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(SponsorTicketsCog(bot))
