"""
Manage Discord UI buttons and interactions.

This module handles button view creation, interaction callbacks, and
persistent registration of views for the bot.
"""

from typing import Any, Callable, Dict, List, Optional, Set

import discord
from discord.ext import commands

from bot.utils.console_logger import console_logger


class ButtonView(discord.ui.View):
    """
    A view that holds interactive or link buttons.
    """

    def __init__(self, buttons: List[Dict[str, Any]], persistent: Optional[bool] = True):
        """
        Initialize a button view.

        Args:
            buttons (List[Dict[str, Any]]): Button definitions.
            persistent (Optional[bool]): Whether the view should persist after restart.

        """
        super().__init__(timeout=None if persistent else 180)
        self.add_buttons(buttons, persistent)

    def add_buttons(self, buttons: List[Dict[str, Any]], persistent: bool):
        """
        Add buttons to the view.

        Args:
            buttons (List[Dict[str, Any]]): Button configurations.
            persistent (bool): Whether persistence is required.

        """
        for btn in buttons:
            if "url" in btn and btn["url"]:
                button = discord.ui.Button(
                    style=btn.get("style", discord.ButtonStyle.link),
                    label=btn.get("label", "Link"),
                    url=btn["url"],
                    emoji=btn.get("emoji"),
                    disabled=btn.get("disabled", False),
                )
                self.add_item(button)
            else:
                custom_id = btn.get("custom_id")
                if not custom_id and persistent:
                    console_logger.error(f"❌ Missing custom_id for persistent button: {btn}")
                    continue
                button = discord.ui.Button(
                    style=btn.get("style", discord.ButtonStyle.secondary),
                    label=btn.get("label", "Button"),
                    custom_id=custom_id,
                    emoji=btn.get("emoji"),
                    disabled=btn.get("disabled", False),
                )
                self.add_item(button)


class ButtonsManager:
    """
    Register persistent button views and interaction callbacks.
    """

    _registered_view_ids: Set[frozenset] = set()
    _button_callbacks: Dict[str, Callable] = {}
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
        async def on_button_interaction(interaction: discord.Interaction):
            """
            Route a button interaction to its callback.

            Args:
                interaction (discord.Interaction): The interaction from Discord.

            """
            if not interaction.data:
                return

            component_type = interaction.data.get("component_type")

            # handle buttons only
            if component_type != discord.ComponentType.button.value:
                return

            custom_id = interaction.data["custom_id"]
            if custom_id in cls._button_callbacks:
                await cls._button_callbacks[custom_id](interaction)
            else:
                await interaction.response.send_message(
                    "⚠️ This feature is disabled or unavailable.",
                    ephemeral=True,
                )

    @classmethod
    def register_callback(cls, custom_id: str, callback: Callable):
        """
        Register a button callback.

        Args:
            custom_id (str): The button's custom ID.
            callback (Callable): The function to invoke.

        """
        cls._button_callbacks[custom_id] = callback

    @classmethod
    def unregister_callback(cls, custom_id: str):
        """
        Unregister a button callback.

        Args:
            custom_id (str): The ID to remove.

        """
        cls._button_callbacks.pop(custom_id, None)

    @classmethod
    def register_view(cls, buttons: List[Dict[str, Any]], persistent: Optional[bool] = True):
        """
        Register a persistent view if not already added.

        Args:
            buttons (List[Dict[str, Any]]): The buttons to register.
            persistent (Optional[bool]): Whether the view is persistent.

        """
        view_id = frozenset((btn.get("custom_id", ""), btn.get("label", "")) for btn in buttons if btn.get("custom_id"))

        if view_id and view_id in cls._registered_view_ids:
            return

        if persistent and any(btn.get("custom_id") for btn in buttons):
            view = ButtonView(buttons, persistent)
            cls._bot.add_view(view)
            cls._registered_view_ids.add(view_id)
