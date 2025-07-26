"""
Prompts Manager Module for handling Discord prompts.

This module provides functionality to manage and send prompts in Discord channels.
It includes a view for displaying prompts in a dropdown menu and methods to send prompts
to channels or interactions.
"""

from typing import List, Optional

import discord

from bot.models.prompt import Prompt
from bot.utils.console_logger import console_logger


class PromptView(discord.ui.View):
    """
    A view that displays prompt suggestions in a dropdown menu.
    """

    def __init__(self, prompts: list[Prompt]):
        """
        Initialize the view with a list of prompts.

        Args:
            prompts (list[Prompt]): A list of Prompt objects to display.

        """
        super().__init__()

        options = [discord.SelectOption(label=prompt.content, value=prompt.custom_id) for prompt in prompts]
        self.add_item(
            discord.ui.Select(
                placeholder="Click Me!",
                options=options,
                custom_id="prompt_suggestion_select",
            )
        )


class PromptsManager:
    """
    Manages sending prompts and handling interactions.
    """

    @classmethod
    async def send_prompt(
        cls,
        *,
        channel: Optional[discord.TextChannel] = None,
        message: str = "Choose a prompt:",
        prompts: List[Prompt] = [],
    ) -> discord.Message:
        """
        Send a prompt to a Discord channel or interaction.

        Args:
            channel (Optional[discord.TextChannel]): The channel to send the prompt to.
            message (str): The message to display with the prompt.
            prompts (List[Prompt]): The list of prompts to include in the message.

        Returns:
            discord.Message: The message object containing the prompt.

        """
        view = PromptView(prompts)
        try:
            if not channel:
                console_logger.error("❌ No channel provided to send the prompt.")
                return

            return await channel.send(message, view=view)
        except Exception as e:
            console_logger.error(f"❌ Failed to send prompt message: {e}")
            return None
