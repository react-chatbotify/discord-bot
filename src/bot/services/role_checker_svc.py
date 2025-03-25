"""
Role checker service module for validating admin and sponsor access.

This module provides utility functions to determine whether a Discord
member has specific roles, such as admin or recurring sponsor roles. It
uses configured role IDs from the bot's settings to perform the checks.
"""

import discord

from bot.config.common import common_config


def is_admin_user(member: discord.Member) -> bool:
    """
    Check if a user has the admin role.

    Args:
        member (discord.Member): The member to check.

    Returns:
        bool: True if the user has the admin role, False otherwise.

    """
    user_roles = {role.id for role in member.roles}
    return common_config.admin_role_id in user_roles


def is_recurring_sponsor_user(member: discord.Member) -> bool:
    """
    Check if a user has any recurring sponsor role.

    Iterates through all configured recurring sponsor tiers and checks
    if the member has a matching role.

    Args:
        member (discord.Member): The member to check.

    Returns:
        bool: True if the user has a recurring sponsor role, False otherwise.

    """
    user_roles = {role.id for role in member.roles}

    for tier in common_config.recurring_sponsor_tiers.values():
        if tier.role_id in user_roles:
            return True

    return False
