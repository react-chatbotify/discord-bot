"""
Prompts Manager Module for handling Discord prompts.

This module provides functionality to manage and send prompts in Discord channels.
It includes a view for displaying prompts in a dropdown menu and methods to send prompts
to channels or interactions.
"""

from typing import Callable, Dict, List, Optional

import discord
from discord.ext import commands

from bot.models.prompt import Prompt
from bot.utils.console_logger import console_logger

# maps the id of a prompt to the text content it shows
PROMPT_ID_TO_TEXT_MAPPING = {}


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

    _prompt_callbacks: Dict[str, Callable] = {}
    _bot: Optional[commands.Bot] = None

    @classmethod
    def setup(cls, bot: commands.Bot):
        """
        Initialize the manager with the bot instance.

        Args:
            bot (commands.Bot): The bot to register listeners on.

        """
        cls._bot = bot

        @bot.listen("on_interaction")
        async def on_prompt_interaction(interaction: discord.Interaction):
            """
            Route a prompt interaction to its callback.

            Args:
                interaction (discord.Interaction): The interaction from Discord.

            """
            if not interaction.data:
                return

            component_type = interaction.data.get("component_type")

            # handle prompts only
            if component_type != discord.ComponentType.select.value:
                return

            custom_id = interaction.data["values"][0]
            if custom_id in cls._prompt_callbacks and not interaction.response.is_done():
                await interaction.response.defer()
                await cls._prompt_callbacks[custom_id](interaction, custom_id)
            else:
                await interaction.response.send_message(
                    "⚠️ This feature is disabled or unavailable.",
                    ephemeral=True,
                )

    @classmethod
    def register_callback(cls, custom_id: str, text: str, callback: Callable):
        """
        Register a prompt callback.

        Args:
            custom_id (str): The prompt's custom ID.
            text (str): The text shown for the prompt.
            callback (Callable): The function to invoke.

        """
        PROMPT_ID_TO_TEXT_MAPPING[custom_id] = text
        cls._prompt_callbacks[custom_id] = callback

    @classmethod
    def unregister_callback(cls, custom_id: str):
        """
        Unregister a prompt callback.

        Args:
            custom_id (str): The ID to remove.

        """
        cls._prompt_callbacks.pop(custom_id, None)

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
