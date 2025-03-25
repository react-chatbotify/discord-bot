"""
Auto voice handler module for managing temporary voice channels.

This module defines logic for creating and deleting temporary voice
channels when members join or leave a designated "Join to Create"
channel. It tracks active temporary channels in memory and manages
permissions and cleanup accordingly.
"""

from typing import Optional

import discord

from bot.config.auto_voice import auto_voice_config

# Tracks temporary voice channels created by the auto-voice system.
# If the bot restarts unexpectedly, lingering channels may not be deleted
# due to the in-memory tracking being reset.
# todo: channels (id) created should be persisted in an auto voice table
temp_channels = {}


async def process_member_join_and_leave_channel(
    member: discord.Member,
    before: Optional[discord.VoiceState],
    after: Optional[discord.VoiceState],
):
    """
    Handle a member joining or leaving a voice channel.

    If a user joins the configured "Join to Create" voice channel, this function
    creates a temporary voice channel for them and grants them appropriate permissions.
    If a tracked temporary channel becomes empty, it is deleted.

    Args:
        member (discord.Member): The member whose voice state changed.
        before (Optional[discord.VoiceState]): The member's previous voice state.
        after (Optional[discord.VoiceState]): The member's new voice state.

    """
    guild = member.guild

    # User joined the "Join to Create" channel
    if after.channel and after.channel.id == auto_voice_config.auto_voice_channel_id:
        template = after.channel
        category = template.category
        new_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Channel",
            user_limit=30,
            category=category,
        )
        await new_channel.set_permissions(member, manage_channels=True, mute_members=True, move_members=True)
        await member.move_to(new_channel)
        temp_channels[new_channel.id] = member.id

    # User left a tracked temporary channel
    if before.channel and before.channel.id in temp_channels:
        if len(before.channel.members) == 0:
            try:
                await before.channel.delete()
                del temp_channels[before.channel.id]
            except Exception as e:
                print(f"Error deleting voice channel: {e}")
