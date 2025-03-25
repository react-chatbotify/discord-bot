"""
User info service module for determining sponsor tier membership.

This module provides utility functions to evaluate which recurring
sponsor tiers a Discord member belongs to, based on role assignments and
the bot's configured sponsorship settings.
"""

from typing import List

import discord

from bot.config.common import common_config


def get_user_recurring_sponsor_tiers(member: discord.Member) -> List[str]:
    """
    Retrieve all recurring sponsor tiers a user belongs to.

    This function checks the member's roles against all configured recurring sponsor tiers
    and returns a list of tier names the user matches. Note: the result is not sorted
    by tier rank.

    Args:
        member (discord.Member): The Discord member to check.

    Returns:
        List[str]: A list of sponsor tier names the user is part of.

    """
    user_roles = {role.id for role in member.roles}

    user_sponsor_tiers = []
    # TODO: Sort result from highest sponsor to lowest sponsor tier
    for tier in common_config.recurring_sponsor_tiers:
        if common_config.recurring_sponsor_tiers[tier].role_id in user_roles:
            user_sponsor_tiers.append(tier)

    return user_sponsor_tiers
