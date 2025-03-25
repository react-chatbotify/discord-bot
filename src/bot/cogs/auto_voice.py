"""
AutoVoiceCog module for dynamic voice channel management.

This module defines a Discord bot cog that listens for voice state
updates and handles the creation and cleanup of temporary voice channels
when users join a designated "Join to Create" channel. The functionality
is aimed at enhancing server voice interactions automatically.
"""

from typing import Optional

import discord
from discord.ext import commands

from bot.core.auto_voice import process_member_join_and_leave_channel


class AutoVoiceCog(commands.Cog):
    """
    A Discord bot cog that manages temporary voice channels.

    This cog automatically creates a new voice channel when a user joins a
    "Join to Create" channel, grants them temporary ownership, and deletes the
    channel when it becomes empty.

    Listeners:
        on_voice_state_update:
            - Creates a temporary voice channel when a user joins the "Join to Create" channel.
            - Deletes the channel when it becomes empty.
    """

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: Optional[discord.VoiceState],
        after: Optional[discord.VoiceState],
    ):
        """
        Handle updates to a member's voice state.

        This listener checks if a member joins or leaves a voice channel and
        triggers logic to create or remove temporary voice channels as needed.

        Args:
            member (discord.Member): The member whose voice state updated.
            before (Optional[discord.VoiceState]): The member's previous voice state.
            after (Optional[discord.VoiceState]): The member's new voice state.

        """
        await process_member_join_and_leave_channel(member, before, after)


async def setup(bot: commands.Bot):
    """
    Set up the AutoVoiceCog by adding it to the bot.

    Args:
        bot (commands.Bot): The bot instance to which the cog is added.

    """
    await bot.add_cog(AutoVoiceCog(bot))
