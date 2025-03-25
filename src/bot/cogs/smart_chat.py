"""
SmartChatCog module for AI-driven smart chat interactions.

This module defines a cog that listens to messages in configured
channels and interacts with an external AI API to generate dynamic
responses. It manages the AI session lifecycle and handles real-time
message processing for enhanced conversation experiences.
"""

import discord
from discord.ext import commands

from bot.config.smart_chat import smart_chat_config
from bot.core.smart_chat import close_session, get_ai_response, start_session


class SmartChatCog(commands.Cog):
    """
    A Discord bot cog that integrates AI-powered smart chat responses.

    This cog sends user messages from specific channels to an external AI API
    and replies with generated responses.

    Listeners:
        on_message:
            - Sends messages to the AI API for processing and replies with the generated response.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the SmartChatCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        self.session = start_session()

    def cog_unload(self):
        """
        Clean up resources when the cog is unloaded.

        This method ensures the session with the external AI service is
        properly closed.
        """
        self.bot.loop.create_task(close_session(self.session))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Handle messages sent in smart chat channels.

        Sends the message content to the AI API and replies with the AI-generated response
        if the message is from a configured smart chat channel.

        Args:
            message (discord.Message): The message sent in the channel.

        """
        # Skip messages from channels not configured for smart chat
        if message.channel.id not in smart_chat_config.smart_chat_channel_ids:
            return

        # Get AI response from the service
        response = await get_ai_response(self.session, message.content)

        # Reply with the response if one was generated
        if response:
            await message.reply(response)


async def setup(bot: commands.Bot):
    """
    Set up the SmartChatCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(SmartChatCog(bot))
