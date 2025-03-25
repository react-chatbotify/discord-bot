"""
BotButton model module for defining Discord button components.

This module contains a Pydantic model that represents the structure and
behavior of a Discord UI button. It includes attributes for label,
style, emoji, interaction callback, and custom ID, and is used to
configure buttons in embed-based views.
"""

from typing import Callable, Optional

import discord
from pydantic import BaseModel, Field


class BotButton(BaseModel):
    """
    Pydantic model representing a Discord button configuration.

    This model defines the attributes required to construct a button component
    in Discord, including its label, style, emoji, and interaction callback.

    Attributes:
        label (str): The text displayed on the button.
        custom_id (str): Unique identifier used to distinguish the button interaction.
        style (discord.ButtonStyle): The visual style of the button (e.g., primary, danger).
        emoji (str): Optional emoji to show alongside the button label.
        callback (Optional[Callable]): A function to execute when the button is clicked.

    """

    label: str = Field(..., description="The text displayed on the button.")
    custom_id: str = Field(..., description="Unique identifier for button interactions.")
    style: discord.ButtonStyle = Field(..., description="Button style (primary, danger, etc.).")
    emoji: str = Field(None, description="Optional emoji displayed on the button.")
    callback: Optional[Callable] = Field(None, description="Optional function to be executed when button is clicked.")

    class Config:
        """
        Pydantic model configuration.
        """

        arbitrary_types_allowed = True
