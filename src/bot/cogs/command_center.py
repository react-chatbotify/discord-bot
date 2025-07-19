"""
CommandCenterCog module for handling critical events and interacting with the MCP server.

This module defines a Discord bot cog that provides administrators with an interface
to communicate with Google Gemini, which in turn has access to a remote MCP
(Model Context Protocol) server.
"""

from discord.ext import commands

from bot.agents.command_center_agent import CommandCenterAgent
from bot.config.command_center import command_center_config
from bot.core.command_center import configure_genai
from bot.services.role_checker_svc import has_admin_role


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

    @commands.command(name="mcp")
    @has_admin_role()
    async def mcp(self, ctx: commands.Context, *, user_request: str):
        """
        Allow administrators to talk to Google Gemini with access to an MCP server.

        Args:
            ctx (commands.Context): The context in which the command is invoked.
            user_request (str): The user's request to be processed by Gemini.

        """
        if ctx.channel.id != int(command_center_config.command_center_channel_id):
            await ctx.send("This command can only be used in the command center channel.")
            return

        async with self.agent as agent:
            response, tool_calls = await agent.get_ai_response(user_request)

            if tool_calls:
                for tool_call in tool_calls:
                    await ctx.send(tool_call, ephemeral=True)

            await ctx.send(response)

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
