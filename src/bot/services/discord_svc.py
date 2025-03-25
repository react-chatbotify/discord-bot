"""
Discord service module for managing channels and permissions.

This module provides utility functions to interact with the Discord API
for creating, deleting, exporting, and managing permissions on text
channels. It includes logic for exporting message history and setting
permission overwrites for roles and members in dynamically generated
channels.
"""

from typing import Any, Dict, List, Optional, Union

import aiofiles
import discord
from discord.ext import commands

from bot.utils.console_logger import console_logger


async def create_channel(
    bot: commands.Bot,
    ctx_or_interaction: Union[commands.Context, discord.Interaction],
    base_name: str,
    category_id: int,
    private: Optional[int] = False,
) -> Optional[discord.TextChannel]:
    """
    Create a new text channel in the specified category.

    Optionally makes the channel private by restricting access to @everyone.

    Args:
        bot (commands.Bot): The bot instance.
        ctx_or_interaction (Union[commands.Context, discord.Interaction]): The context or interaction.
        base_name (str): The name to give the new channel.
        category_id (int): The ID of the category to place the channel in.
        private (Optional[int]): Whether the channel should be private. Defaults to False.

    Returns:
        Optional[discord.TextChannel]: The created channel, or None on failure.

    """
    guild = ctx_or_interaction.guild
    category = await _get_category(bot, ctx_or_interaction, category_id)
    if not category:
        return None

    bot_member = guild.get_member(bot.user.id)
    if not category.permissions_for(bot_member).manage_channels:
        return None

    try:
        channel = await guild.create_text_channel(name=base_name, category=category)
        if private:
            await set_role_channel_permissions(
                channel,
                role_permissions=[
                    {
                        "roles": guild.default_role,
                        "permissions": {"read_messages": False},
                    }
                ],
            )
        console_logger.info(f"✅ Created channel {channel.name} in category {category.name}")
        return channel
    except Exception as e:
        console_logger.error(f"❌ Error creating channel: {str(e)}")
        return None


async def delete_channel(
    bot: commands.Bot,
    guild: discord.Guild,
    channel_id: int,
) -> bool:
    """
    Delete a text channel by its ID.

    Args:
        bot (commands.Bot): The bot instance.
        guild (discord.Guild): The guild containing the channel.
        channel_id (int): The ID of the channel to delete.

    Returns:
        bool: True if deleted successfully, False otherwise.

    """
    channel = guild.get_channel(channel_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(channel_id)
        except discord.NotFound:
            console_logger.error(f"❌ Channel ID {channel_id} not found.")
            return False
        except discord.Forbidden:
            console_logger.error(f"🚫 Missing permissions to fetch channel ID {channel_id}.")
            return False

    try:
        await channel.delete()
        console_logger.info(f"🗑️ Deleted channel {channel.name} ({channel.id})")
        return True
    except discord.Forbidden:
        console_logger.error(f"🚫 Missing permissions to delete channel {channel.name} ({channel.id})")
    except discord.HTTPException as e:
        console_logger.error(f"❌ Error deleting channel {channel.name} ({channel.id}): {str(e)}")

    return False


async def set_role_channel_permissions(
    channel: discord.TextChannel,
    role_permissions: List[Dict[str, Union[discord.Role, List[discord.Role], Dict[str, Any]]]],
) -> None:
    """
    Set permission overwrites for one or more roles in a channel.

    Args:
        channel (discord.TextChannel): The channel to update.
        role_permissions (List[Dict]): List of role/permissions pairs.

    """
    overwrites = channel.overwrites
    for item in role_permissions:
        roles = item.get("roles")
        perms = item.get("permissions")
        if not isinstance(roles, list):
            roles = [roles]
        if isinstance(perms, dict):
            perms = discord.PermissionOverwrite(**perms)
        for role in roles:
            overwrites[role] = perms
    try:
        await channel.edit(overwrites=overwrites)
        console_logger.info(f"🔑 Updated role permissions for channel {channel.name}")
    except Exception as e:
        console_logger.error(f"❌ Failed to update role permissions for channel {channel.name}: {e}")


async def set_member_channel_permissions(
    channel: discord.TextChannel,
    member_permissions: List[Dict[str, Union[discord.Member, List[discord.Member], Dict[str, Any]]]],
) -> None:
    """
    Set permission overwrites for one or more members in a channel.

    Args:
        channel (discord.TextChannel): The channel to update.
        member_permissions (List[Dict]): List of member/permissions pairs.

    """
    overwrites = channel.overwrites
    for item in member_permissions:
        members = item.get("members")
        perms = item.get("permissions")
        if not isinstance(members, list):
            members = [members]
        if isinstance(perms, dict):
            perms = discord.PermissionOverwrite(**perms)
        for member in members:
            overwrites[member] = perms
    try:
        await channel.edit(overwrites=overwrites)
        console_logger.info(f"🔑 Updated member permissions for channel {channel.name}")
    except Exception as e:
        console_logger.error(f"❌ Failed to update member permissions for channel {channel.name}: {e}")


async def export_channel_contents(
    bot: commands.Bot,
    target_channel_id: int,
    download_channel_id: int,
    include_asset_urls: Optional[bool] = True,
) -> None:
    """
    Export and send the message history of a channel as a text file.

    Args:
        bot (commands.Bot): The bot instance.
        target_channel_id (int): The ID of the channel to export.
        download_channel_id (int): The ID of the channel to send the file in.
        include_asset_urls (Optional[bool]): Whether to include URLs for attachments and embeds.

    """
    target_channel = bot.get_channel(target_channel_id)
    download_channel = bot.get_channel(download_channel_id)

    if not target_channel or not download_channel:
        console_logger.error("❌ Invalid target or download channel ID provided.")
        return

    messages = []
    try:
        async for message in target_channel.history(limit=None, oldest_first=True):
            msg_text = f"[{message.created_at}] {message.author.display_name}: {message.content}"

            if message.attachments and include_asset_urls:
                attachment_urls = [f"\n- Attachment: {a.url}" for a in message.attachments]
                msg_text += "\n" + "\n".join(attachment_urls)

            if message.embeds and include_asset_urls:
                for i, embed in enumerate(message.embeds):
                    msg_text += f"\n- Embed {i + 1}:"
                    if embed.title:
                        msg_text += f"\n  Title: {embed.title}"
                    if embed.description:
                        msg_text += f"\n  Description: {embed.description}"
                    for field in embed.fields:
                        msg_text += f"\n  Field - {field.name}: {field.value}"
                    if embed.image:
                        msg_text += f"\n  Image: {embed.image.url}"
                    if embed.thumbnail:
                        msg_text += f"\n  Thumbnail: {embed.thumbnail.url}"

            messages.append(msg_text)

        if not messages:
            await download_channel.send("ℹ️ No messages found in the target channel.")
            return

        file_name = f"chat_history_{target_channel.name}.txt"
        async with aiofiles.open(file_name, mode="w", encoding="utf-8") as file:
            await file.write("\n\n".join(messages))

        await download_channel.send(
            f"📁 Here is the chat history of **#{target_channel.name}**:"
            + (
                "\n⚠️ **Note:** This log includes URLs to attachments and images. "
                "Please download any important files now, as they will become inaccessible when the channel is deleted."
                if include_asset_urls
                else ""
            ),
            file=discord.File(file_name),
        )

        console_logger.info(f"✅ Successfully exported chat history from {target_channel.name}")

    except discord.Forbidden:
        console_logger.error("🚫 Missing permissions to read messages or send files.")
    except Exception as e:
        console_logger.error(f"❌ Error exporting chat history: {e}")


async def _get_category(
    bot: commands.Bot,
    ctx: Union[commands.Context, discord.Interaction],
    category_id: int,
) -> Optional[discord.CategoryChannel]:
    """
    Fetch a category channel by its ID.

    Args:
        bot (commands.Bot): The bot instance.
        ctx (Union[commands.Context, discord.Interaction]): The context or interaction object.
        category_id (int): The ID of the category.

    Returns:
        Optional[discord.CategoryChannel]: The category channel, or None if not found or invalid.

    """
    guild = ctx.guild
    category = guild.get_channel(category_id)
    if category is None:
        try:
            category = await bot.fetch_channel(category_id)
        except Exception:
            return None
    if not isinstance(category, discord.CategoryChannel):
        return None
    return category
