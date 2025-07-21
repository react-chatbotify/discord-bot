"""
CommandCenterCog module for handling critical events and interacting with the MCP server.

This module defines a Discord bot cog that provides administrators with an interface
to communicate with Google Gemini, which in turn has access to a remote MCP
(Model Context Protocol) server.
"""

import discord
from discord.ext import commands

from bot.agents.command_center_agent import CommandCenterAgent
from bot.config.command_center import command_center_config
from bot.core.command_center import configure_genai
from bot.utils.decorators import admin_only


class CommandCenter(commands.Cog):
    """
    A Discord bot cog for processing and routing command center events
    and interacting with the MCP server.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the CommandCenterCog.

        Args:
            bot (commands.Bot): The Discord bot instance.

        """
        self.bot = bot
        self.agent = CommandCenterAgent()
        configure_genai()

    # todo: need to restrict to admin role?
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Trigger MCP logic when a message is sent in the command center channel and the bot is mentioned.
        """
        # Ignore bot's own messages
        if message.author.bot:
            return

        # Only act in the command center channel
        if message.channel.id != int(command_center_config.command_center_channel_id):
            return

        # Only proceed if the bot is mentioned
        if self.bot.user not in message.mentions:
            return

        user_request = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not user_request:
            await message.channel.send("Please include a request after mentioning the bot.")
            return

        async with self.agent as agent:
            response, tool_calls = await agent.get_ai_response(user_request)

            if tool_calls:
                for tool_call in tool_calls:
                    await message.channel.send(tool_call)

            await message.channel.send(response)

    @commands.Cog.listener()
    async def on_service_issue_event(self, data: dict):
        """
        Handle an external webhook event dispatched by the bot to indicate a service issue.

        Args:
            data (dict): The event payload containing at least a 'message' field.

        """
        channel_id = command_center_config.command_center_channel_id
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                message = data.get("message", "No message provided.")
                await channel.send(f"Webhook event received: {message}")


async def setup(bot: commands.Bot):
    """
    Set up the CommandCenterCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(CommandCenter(bot))
