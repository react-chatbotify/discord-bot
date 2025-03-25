"""
SponsorTier model module for defining sponsorship tier metadata.

This module provides a Pydantic model representing a sponsor tier,
including its name, emoji, and associated Discord role ID. It is used
for configuring and identifying sponsor roles across the bot.
"""

from pydantic import BaseModel, Field


class SponsorTier(BaseModel):
    """
    Represents a sponsorship tier with its metadata and associated role.

    This model defines the structure of a sponsor tier, including its name,
    emoji representation, and corresponding Discord role ID.

    Attributes:
        name (str): The name of the sponsor tier (e.g., "Bronze", "Platinum").
        emoji (str): A short emoji string representing the tier.
        role_id (int): The Discord role ID associated with this tier.

    """

    name: str = Field(..., min_length=3, max_length=20, description="The name of the sponsor tier.")
    emoji: str = Field(..., min_length=1, max_length=2, description="The emoji representing the tier.")
    role_id: int = Field(..., gt=0, description="The Discord role ID associated with this tier.")
