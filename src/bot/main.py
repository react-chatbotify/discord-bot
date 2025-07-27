"""
Main entry point for the Discord bot.

This script initializes the bot instance, loads environment variables,
sets up cogs, connects to the database, and launches the bot.

Features:
- Loads all cogs on startup
- Loads all buttons (register callbacks/views)
- Initializes database tables
- Sets up slash commands
- Logs bot readiness to the console
"""

import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.cogs.cogs_manager import CogsManager
from bot.database.mysql.init_db import init_db
from bot.database.mysql.ticket_counter import initialize_ticket_counter_table
from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.ui.prompts.prompts_manager import PromptsManager
from bot.utils.console_logger import console_logger
from bot.web_server import WebServer

# Load environment variables from .env
load_dotenv()

# Create bot with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up all buttons (register callbacks)
ButtonsManager.setup(bot)

# Set up all prompts (register callbacks)
PromptsManager.setup(bot)

# Initialize cog manager
cogs_manager = CogsManager(bot)

# Flag if bot startup is complete
bot_startup_complete = False

# Web server instance
web_server = WebServer(bot)


@bot.event
async def on_ready():
    """
    Handle bot ready event.
    """
    # Run logic only if bot startup is incomplete
    global bot_startup_complete
    if not bot_startup_complete:
        console_logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

        # Initialize DB and ticket counters
        await init_db()
        bot.loop.create_task(initialize_ticket_counter_table())

        # Load all cogs
        await cogs_manager.load_all_cogs()

        # Log readiness and available commands
        console_logger.info(f"Bot is ready with {len(bot.tree.get_commands())} command(s) loaded:")
        for cmd in bot.tree.get_commands():
            console_logger.info(f"Command loaded: {cmd.name}")

        bot_startup_complete = True
    else:
        console_logger.info("Reconnected to Discord.")


async def main():
    """
    Handle initialization of the bot and web server.
    """
    async with bot:
        await web_server.start()
        await bot.start(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console_logger.info("Bot is shutting down.")
