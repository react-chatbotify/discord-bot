"""
Embed manager module for handling embeds and button callbacks.

This module provides an interface for sending embeds with dynamic and
persistent buttons in Discord. It handles view registration, interaction
dispatching, and responds appropriately to context or interaction
sources.
"""

from typing import Any, Dict, List, Optional, Union

import discord
from discord.ext import commands

from bot.ui.buttons.buttons_manager import ButtonsManager
from bot.utils.console_logger import console_logger


class ButtonView(discord.ui.View):
    """
    A dynamic Discord UI view for handling interactive buttons.
    """

    def __init__(self, buttons: List[Dict[str, Any]], persistent: Optional[bool] = True):
        """
        Initialize the view with a list of buttons.

        Args:
            buttons (List[Dict[str, Any]]): A list of button configurations.
            persistent (Optional[bool]): Whether the buttons should persist
                after bot restart. Defaults to True.

        """
        super().__init__(timeout=None if persistent else 180)
        self.add_buttons(buttons, persistent)

    def add_buttons(self, buttons: List[Dict[str, Any]], persistent: bool):
        """
        Dynamically add buttons to the view.

        Args:
            buttons (List[Dict[str, Any]]): A list of button configurations.
            persistent (bool): Whether the buttons should persist after restart.

        """
        for btn in buttons:
            if "url" in btn and btn["url"]:
                button = discord.ui.Button(
                    style=btn.get("style", discord.ButtonStyle.link),
                    label=btn.get("label", "Link"),
                    url=btn["url"],
                    emoji=btn.get("emoji", None),
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
                    emoji=btn.get("emoji", None),
                    disabled=btn.get("disabled", False),
                )
                self.add_item(button)


class EmbedsManager:
    """
    Manages sending embeds and button interactions for the Discord bot.
    """

    @classmethod
    async def send_embed(
        cls,
        ctx_or_interaction: Union[commands.Context, discord.Interaction],
        *,
        channel: Optional[discord.TextChannel] = None,  # Optional[discord.TextChannel]
        title: Optional[str] = None,  # Optional[str]
        description: Optional[str] = None,  # Optional[str]
        color: Optional[int] = discord.Color.blue().value,  # Optional[int]
        thumbnail_url: Optional[str] = None,  # Optional[str]
        image_url: Optional[str] = None,  # Optional[str]
        author_name: Optional[str] = None,  # Optional[str]
        author_icon_url: Optional[str] = None,  # Optional[str]
        footer_text: Optional[str] = None,  # Optional[str]
        footer_icon_url: Optional[str] = None,  # Optional[str]
        fields: Optional[List[Dict[str, str]]] = None,  # Optional[List[Dict[str, str]]]
        buttons: Optional[List[Dict[str, Any]]] = None,  # Optional[List[Dict[str, Any]]]
        persistent: Optional[bool] = True,
        ephemeral: Optional[bool] = False,
        file: Optional[discord.File] = None,  # Optional[discord.File]
    ) -> discord.Message:
        """
        Send an embed to a Discord channel or interaction.

        Args:
            ctx_or_interaction (Union[commands.Context, discord.Interaction]):
                The context or interaction from which to send the embed.
            channel (Optional[discord.TextChannel], optional): Channel to send to, overrides default.
            title (str, optional): Embed title.
            description (str, optional): Embed description.
            color (int, optional): Embed color. Defaults to blue.
            thumbnail_url (str, optional): URL of the thumbnail image.
            image_url (str, optional): URL of the main image.
            author_name (str, optional): Author text.
            author_icon_url (str, optional): Author icon URL.
            footer_text (str, optional): Footer text.
            footer_icon_url (str, optional): Footer icon URL.
            fields (List[Dict[str, str]], optional): List of field dicts (name, value).
            buttons (List[Dict[str, Any]], optional): List of button dicts.
            persistent (Optional[bool]): Whether buttons should persist. Defaults to True.
            ephemeral (Optional[bool]): Whether response is ephemeral. Defaults to False.
            file (discord.File, optional): File to send with the embed.

        Returns:
            discord.Message: The message object containing the embed.

        """
        # If buttons are provided and persistence is desired, register the view via ButtonsManager.
        if buttons and persistent and ButtonsManager._bot:
            ButtonsManager.register_view(buttons, persistent)

        # Build the embed.
        embed = discord.Embed(title=title, description=description, color=color)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if image_url:
            embed.set_image(url=image_url)
        if author_name:
            embed.set_author(name=author_name, icon_url=author_icon_url)
        if footer_text:
            embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        if fields:
            for field in fields:
                embed.add_field(
                    name=field["name"],
                    value=field["value"],
                    inline=field.get("inline", False),
                )

        # Create a view if buttons were provided.
        view = ButtonView(buttons, persistent) if buttons else None

        # Dispatch the embed message based on context type.
        if channel:
            kwargs = {"embed": embed, "view": view}
            if file:
                kwargs["file"] = file
            return await channel.send(**kwargs)

        kwargs = {"embed": embed, "view": view, "ephemeral": ephemeral}
        if file:
            kwargs["file"] = file

        if isinstance(ctx_or_interaction, commands.Context):
            return await ctx_or_interaction.send(**kwargs)

        await ctx_or_interaction.response.send_message(**kwargs)
        return await ctx_or_interaction.original_response()
