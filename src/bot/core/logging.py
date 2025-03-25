"""
Logging handlers module for recording Discord server events.

This module provides core functionality to log key server events such as
message deletions and edits, channel creation and deletion, member
join/leave events, and voice state changes. Log messages are formatted
and sent to a configured Discord logging channel using the bot's
settings.
"""

import discord

from bot.config.logging import logging_config


async def log_to_channel(bot, content: str):
    """
    Send a log message to the configured Discord log channel.

    Args:
        bot: The Discord bot instance.
        content (str): The message content to send.

    """
    channel = bot.get_channel(logging_config.log_channel_id)
    if channel:
        await channel.send(content)


async def handle_message_delete(bot, message: discord.Message):
    """
    Log a message deletion event.

    Args:
        bot: The Discord bot instance.
        message (discord.Message): The deleted message.

    """
    if message.author.bot:
        return
    log_msg = (
        f"❌ Message deleted | #{message.channel.name} | " f"{message.author.display_name}\n```{message.content}```"
    )
    await log_to_channel(bot, log_msg)


async def handle_message_edit(bot, before: discord.Message, after: discord.Message):
    """
    Log a message edit event.

    Args:
        bot: The Discord bot instance.
        before (discord.Message): The message before editing.
        after (discord.Message): The message after editing.

    """
    if before.author.bot or before.content == after.content:
        return
    log_msg = (
        f"📝 Message edited | #{before.channel.name} | {before.author.display_name}\n"
        f"**Before:**\n```{before.content}```\n**After:**\n```{after.content}```"
    )
    await log_to_channel(bot, log_msg)


async def handle_channel_create(bot, channel: discord.abc.GuildChannel):
    """
    Log when a new channel is created.

    Args:
        bot: The Discord bot instance.
        channel (discord.abc.GuildChannel): The newly created channel.

    """
    log_msg = f"➕ Channel created | #{channel.name} | ID: {channel.id}"
    await log_to_channel(bot, log_msg)


async def handle_channel_delete(bot, channel: discord.abc.GuildChannel):
    """
    Log when a channel is deleted.

    Args:
        bot: The Discord bot instance.
        channel (discord.abc.GuildChannel): The deleted channel.

    """
    log_msg = f"➖ Channel deleted | #{channel.name} | ID: {channel.id}"
    await log_to_channel(bot, log_msg)


async def handle_voice_state_update(
    bot,
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
):
    """
    Log changes to a member's voice channel state.

    This includes joining, leaving, or moving between voice channels.

    Args:
        bot: The Discord bot instance.
        member (discord.Member): The member whose voice state changed.
        before (discord.VoiceState): The previous voice state.
        after (discord.VoiceState): The updated voice state.

    """
    if before.channel is None and after.channel is not None:
        log_msg = f"🔊 Voice | {member.display_name} joined {after.channel.name}"
    elif before.channel is not None and after.channel is None:
        log_msg = f"🔊 Voice | {member.display_name} left {before.channel.name}"
    elif before.channel != after.channel:
        log_msg = f"🔊 Voice | {member.display_name} moved: " f"{before.channel.name} → {after.channel.name}"
    else:
        return
    await log_to_channel(bot, log_msg)


async def handle_member_join(bot, member: discord.Member):
    """
    Log when a member joins the guild.

    Args:
        bot: The Discord bot instance.
        member (discord.Member): The member who joined.

    """
    log_msg = f"➕ Member joined | {member.display_name} | ID: {member.id}"
    await log_to_channel(bot, log_msg)


async def handle_member_remove(bot, member: discord.Member):
    """
    Log when a member leaves the guild.

    Args:
        bot: The Discord bot instance.
        member (discord.Member): The member who left.

    """
    log_msg = f"➖ Member left | {member.display_name} | ID: {member.id}"
    await log_to_channel(bot, log_msg)
