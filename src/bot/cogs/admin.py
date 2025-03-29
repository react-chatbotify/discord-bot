"""
AdminCog module for managing administrative bot commands.

This module defines a Discord bot cog that provides various
administrative commands such as enabling/disabling modules and syncing
application commands. Intended for use by bot administrators only.
"""

from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from bot.button_loaders.common import CommonButtonLoader
from bot.cogs.cogs_manager import CogsManager
from bot.core.admin import process_list_modules, process_sync_commands
from bot.utils.console_logger import console_logger
from bot.utils.decorators import admin_only


class AdminCog(commands.Cog):
    """
    A Discord bot cog that provides administrative commands.

    This cog allows server admins to manage bot modules dynamically and sync
    application commands.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        cogs_manager (CogsManager): Manager for loading/unloading cogs.

    Commands:
        /module list:
            - List all bot modules and their status.

        /module enable <name>:
            - Enable a specific bot module.

        /module disable <name>:
            - Disable a specific bot module.

        /sync_commands:
            - Syncs slash commands to the Discord API for this server.

    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the AdminCog.

        Args:
            bot (commands.Bot): The bot instance to attach the cog to.

        """
        self.bot = bot
        self.cogs_manager = CogsManager(bot)
        CommonButtonLoader.load_buttons()

    async def _get_available_cogs(self) -> List[str]:
        """
        Retrieve a list of available cog names.

        Returns:
            List[str]: A list of cog names (not full dotted paths).

        """
        return [cog.split(".")[-1] for cog in self.cogs_manager.cogs]

    module_group = app_commands.Group(name="module", description="Manage bot modules")

    async def _module_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        """
        Provide autocomplete options for module names.

        Args:
            interaction (discord.Interaction): The Discord interaction context.
            current (str): The current partial input string.

        Returns:
            List[app_commands.Choice[str]]: A list of autocomplete suggestions.

        """
        cogs = await self._get_available_cogs()
        return [app_commands.Choice(name=cog, value=cog) for cog in cogs if current.lower() in cog.lower()][
            :25
        ]  # Discord has a limit of 25 choices

    @module_group.command(name="list", description="List all bot modules and their status")
    @admin_only()
    @commands.guild_only()
    async def module_list(self, interaction: discord.Interaction):
        """
        List all bot modules and display their enable/disable status.

        Args:
            interaction (discord.Interaction): The interaction instance.

        """
        await process_list_modules(interaction, self.bot, self.cogs_manager)

    @module_group.command(name="enable", description="Enable a specific bot module")
    @app_commands.describe(module="The name of the module to enable")
    @app_commands.autocomplete(module=_module_name_autocomplete)
    @admin_only()
    @commands.guild_only()
    async def module_enable(self, interaction: discord.Interaction, module: str):
        """
        Enable a specific bot module.

        Args:
            interaction (discord.Interaction): The interaction instance.
            module (str): The name of the module to enable.

        """
        await self.cogs_manager.enable_cog(module)

    @module_group.command(name="disable", description="Disable a specific bot module")
    @app_commands.describe(module="The name of the module to disable")
    @app_commands.autocomplete(module=_module_name_autocomplete)
    @admin_only()
    @commands.guild_only()
    async def module_disable(self, interaction: discord.Interaction, module: str):
        """
        Disable a specific bot module.

        Args:
            interaction (discord.Interaction): The interaction instance.
            module (str): The name of the module to disable.

        """
        await self.cogs_manager.disable_cog(module)

    @app_commands.command(
        name="sync_commands",
        description="Sync slash commands to this server (Admin Only)",
    )
    @admin_only()
    @commands.guild_only()
    async def sync_commands(self, interaction: discord.Interaction):
        """
        Sync slash commands with Discord's API for this guild only.

        Args:
            interaction (discord.Interaction): The interaction instance.

        """
        ctx = await commands.Context.from_interaction(interaction)
        await process_sync_commands(ctx)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """
        Trigger when bot joins a server.

        Args:
            guild (discord.Guild): The server that the bot is joining.

        """
        try:
            await self.bot.tree.sync(guild=guild)
            console_logger.info(f"Synced commands for guild: {guild.name} ({guild.id})")
        except Exception as e:
            console_logger.info(f"Failed to sync commands for guild {guild.name}: {e}")


async def setup(bot: commands.Bot):
    """
    Set up the AdminCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(AdminCog(bot))
