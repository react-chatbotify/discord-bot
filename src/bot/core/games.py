"""
Game logic module for counting and collaborative storytelling games.

This module provides the backend logic for two interactive Discord games:
a counting game that enforces numeric order and a storytelling game that
prevents users from posting consecutively. It handles message validation,
deletion, and simple rule enforcement in designated channels.
"""

import discord


async def handle_counting_game(message: discord.Message):
    """
    Handle the counting game logic by validating the user's number.

    This function checks whether the number posted by the user is the next
    valid number in the counting sequence. If not, the message is deleted
    and a warning is sent.

    Args:
        message (discord.Message): The message sent by the user.

    Returns:
        bool: True if the count was valid, False otherwise.

    """
    try:
        current_number = int(message.content.strip())
    except ValueError:
        await message.delete()
        await message.channel.send(
            "Oops! You counted wrong! Please use a valid number.",
            delete_after=3,
        )
        return

    previous_number = await _get_previous_valid_count(message.channel)
    expected_number = previous_number + 1 if previous_number is not None else 1

    if current_number != expected_number:
        await message.delete()
        await message.channel.send(
            f"Oops! You counted wrong! The next number should be {expected_number}.",
            delete_after=3,
        )


async def _get_previous_valid_count(channel: discord.TextChannel):
    """
    Get the most recent valid number in the counting game.

    This function searches the message history for the latest valid count
    that was not sent by a bot.

    Args:
        channel (discord.TextChannel): The channel to search in.

    Returns:
        int | None: The most recent valid number found, or None if none found.

    """
    async for message in channel.history(limit=50):
        if message.author.bot:
            continue
        try:
            number = int(message.content.strip())
            return number
        except ValueError:
            continue
    return None


async def handle_story_game(message: discord.Message):
    """
    Handle the collaborative story game logic.

    Ensures that users do not post consecutive messages in the story channel.

    Args:
        message (discord.Message): The message sent by the user.

    Returns:
        bool: True if the message was allowed, False if deleted due to rule violation.

    """
    messages = await message.channel.history(limit=2).flatten()

    if len(messages) < 2:
        return

    last_message = messages[1]  # messages[0] is the current one

    if last_message.author.id == message.author.id:
        await message.delete()
        await message.channel.send("Let others share their story!", delete_after=3)
