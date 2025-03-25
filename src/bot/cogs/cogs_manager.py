"""
CogsManager module for dynamic loading and management of bot extensions.

This module defines the CogsManager class, which allows the bot to load,
enable, and disable cog modules at runtime. It helps manage core bot
functionality and modular feature sets.
"""

from discord.ext import commands

from bot.config.cogs_manager import cogs_manager_config
from bot.utils.console_logger import console_logger


class CogsManager:
    """
    Manages loading, enabling, and disabling of bot cogs.

    This utility class is used to handle dynamic cog management for the bot,
    including startup loading and runtime toggling of specific modules.

    Attributes:
        bot (commands.Bot): The bot instance that manages the cogs.

    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the CogsManager.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot

    async def load_all_cogs(self):
        """
        Load all cogs at bot startup.

        Iterates over the configured list of cog modules and attempts to
        load each one. Logs success or failure to the console.
        """
        for cog in cogs_manager_config.loaded_modules:
            cog = f"bot.cogs.{cog}"
            try:
                await self.bot.load_extension(cog)
                console_logger.info(f"✅ Loaded {cog}")
            except Exception as e:
                console_logger.info(f"❌ Failed to load {cog}: {e}")

    async def enable_cog(self, cog_name: str):
        """
        Enable a cog dynamically by name.

        Args:
            cog_name (str): The name of the cog to enable (e.g. 'games').

        Returns:
            str: A status message indicating success or failure.

        """
        cog_path = f"bot.cogs.{cog_name}"
        if cog_path in self.bot.extensions:
            return f"Cog `{cog_name}` is already enabled."
        try:
            await self.bot.load_extension(cog_path)
            return f"✅ Enabled `{cog_name}`"
        except Exception as e:
            return f"❌ Failed to enable `{cog_name}`: {e}"

    async def disable_cog(self, cog_name: str):
        """
        Disable a cog dynamically by name.

        Args:
            cog_name (str): The name of the cog to disable (e.g. 'games').

        Returns:
            str: A status message indicating success or failure.

        """
        cog_path = f"bot.cogs.{cog_name}"
        if cog_path not in self.bot.extensions:
            return f"Cog `{cog_name}` is not enabled."
        try:
            await self.bot.unload_extension(cog_path)
            return f"🚫 Disabled `{cog_name}`"
        except Exception as e:
            return f"❌ Failed to disable `{cog_name}`: {e}"
