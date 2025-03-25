"""
GamesCog module for managing interactive Discord games.

This module defines a cog that implements simple text-based games within
Discord channels, including a counting game and a collaborative
storytelling game. It listens for messages and applies game-specific
logic based on configured channel IDs.
"""

import discord
from discord.ext import commands

from bot.config.games import games_config
from bot.core.games import handle_counting_game, handle_story_game


class GamesCog(commands.Cog):
    """
    A Discord bot cog that provides interactive games.

    This cog manages a counting game where users must count sequentially and a
    story game where users contribute to a collaborative story.

    Listeners:
        on_message:
            - Enforces correct counting in the counting game.
            - Prevents consecutive messages by the same user in the story game.
    """

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Handle incoming messages and route to the appropriate game logic.

        This listener processes messages in specific channels and triggers
        game logic for counting or storytelling games.

        Args:
            message (discord.Message): The message sent in the server.

        """
        if message.author.bot:
            return

        if message.channel.id == games_config.count_channel_id:
            await handle_counting_game(message)
            return

        if message.channel.id == games_config.story_channel_id:
            await handle_story_game(message)


async def setup(bot: commands.Bot):
    """
    Set up the GamesCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(GamesCog(bot))
