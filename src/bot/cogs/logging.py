"""
LoggingCog module for tracking Discord server events.

This module defines a cog that listens to various server events such as
message deletions and edits, member joins and leaves, channel changes,
and voice state updates. It delegates event handling to core logging
functions for centralized log processing.
"""

import discord
from discord.ext import commands

from bot.config.logging import logging_config
from bot.core.logging import (
    handle_channel_create,
    handle_channel_delete,
    handle_member_join,
    handle_member_remove,
    handle_message_delete,
    handle_message_edit,
    handle_voice_state_update,
)


class LoggingCog(commands.Cog):
    """
    A Discord bot cog that logs server events.

    This cog logs message deletions, edits, channel creations/deletions, voice activity,
    and member joins/leaves.

    Listeners:
        on_message_delete:
            - Logs deleted messages (excluding bot messages).

        on_message_edit:
            - Logs edited messages.

        on_guild_channel_create:
            - Logs when a channel is created.

        on_guild_channel_delete:
            - Logs when a channel is deleted.

        on_voice_state_update:
            - Logs when a user joins, leaves, or moves between voice channels.

        on_member_join:
            - Logs when a new member joins the server.

        on_member_remove:
            - Logs when a member leaves the server.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initialize the LoggingCog.

        Args:
            bot (commands.Bot): The bot instance to which the cog is added.

        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        Log a deleted message.

        Args:
            message (discord.Message): The deleted message object.

        """
        if "message_delete" in logging_config.logged_actions:
            await handle_message_delete(self.bot, message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """
        Log a message edit event.

        Args:
            before (discord.Message): The original message before editing.
            after (discord.Message): The updated message after editing.

        """
        if "message_edit" in logging_config.logged_actions:
            await handle_message_edit(self.bot, before, after)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """
        Log when a channel is created.

        Args:
            channel (discord.abc.GuildChannel): The created channel.

        """
        if "channel_create" in logging_config.logged_actions:
            await handle_channel_create(self.bot, channel)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """
        Log when a channel is deleted.

        Args:
            channel (discord.abc.GuildChannel): The deleted channel.

        """
        if "channel_delete" in logging_config.logged_actions:
            await handle_channel_delete(self.bot, channel)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        """
        Log voice channel state changes for a member.

        Args:
            member (discord.Member): The member whose voice state changed.
            before (discord.VoiceState): The member's previous voice state.
            after (discord.VoiceState): The member's new voice state.

        """
        if "voice_state_update" in logging_config.logged_actions:
            await handle_voice_state_update(self.bot, member, before, after)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Log when a member joins the server.

        Args:
            member (discord.Member): The member who joined.

        """
        if "member_join" in logging_config.logged_actions:
            await handle_member_join(self.bot, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Log when a member leaves the server.

        Args:
            member (discord.Member): The member who left.

        """
        if "member_remove" in logging_config.logged_actions:
            await handle_member_remove(self.bot, member)


async def setup(bot: commands.Bot):
    """
    Set up the LoggingCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(LoggingCog(bot))
