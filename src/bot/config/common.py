"""
CommonConfig module for shared bot configuration and sponsor tier settings.

This module defines core configuration settings for the bot, including
module loading, ticket system categories, admin roles, and sponsor tier
definitions. It uses Pydantic for environment-based validation and
supports both one-off and recurring sponsorship structures.
"""

import os
from typing import Dict

from pydantic import Field
from pydantic_settings import BaseSettings

from bot.models.sponsor_tier import SponsorTier


class CommonConfig(BaseSettings):
    """
    Common configuration settings for core bot functionality.

    This includes module loading, ticket system category IDs, admin roles,
    and definitions for sponsor tiers.

    Attributes:
        loaded_modules (str): A comma-separated list of module names to load.
        sponsor_tickets_category_id (int): Category ID where sponsor tickets are created.
        report_tickets_category_id (int): Category ID where report tickets are created.
        admin_role_id (int): Role ID for users with admin access.
        one_off_sponsor_tiers (Dict[str, SponsorTier]): One-time sponsorship tier definitions.
        recurring_sponsor_tiers (Dict[str, SponsorTier]): Recurring sponsorship tier definitions.

    """

    loaded_modules: str = Field(
        default="",
        description="A comma-separated string of module names to be loaded at runtime.",
    )
    sponsor_tickets_category_id: int = Field(
        default=0,
        description="The Discord category ID where sponsor tickets are created.",
    )
    report_tickets_category_id: int = Field(
        default=0,
        description="The Discord category ID where report tickets are created.",
    )
    admin_role_id: int = Field(
        default=0,
        description="The Discord role ID that designates admin users.",
    )

    one_off_sponsor_tiers: Dict[str, SponsorTier] = {
        "community": SponsorTier(
            name="Community",
            emoji="🤝",
            role_id=int(os.getenv("COMMUNITY_SPONSOR_ROLE_ID", 0)),
        ),
    }
    recurring_sponsor_tiers: Dict[str, SponsorTier] = {
        "lite": SponsorTier(
            name="Lite",
            emoji="🥉",
            role_id=int(os.getenv("LITE_SPONSOR_ROLE_ID", 0)),
        ),
        "plus": SponsorTier(
            name="Plus",
            emoji="🥈",
            role_id=int(os.getenv("PLUS_SPONSOR_ROLE_ID", 0)),
        ),
        "pro": SponsorTier(
            name="Pro",
            emoji="🥇",
            role_id=int(os.getenv("PRO_SPONSOR_ROLE_ID", 0)),
        ),
        "ultra": SponsorTier(
            name="Ultra",
            emoji="🏆",
            role_id=int(os.getenv("ULTRA_SPONSOR_ROLE_ID", 0)),
        ),
    }


common_config = CommonConfig()
