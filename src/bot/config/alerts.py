"""
Alerts module for managing webhook alerts.

This module defines configuration settings for receiving webhook alerts.
"""

from typing import Dict

import discord
from pydantic import Field
from pydantic_settings import BaseSettings


class AlertsConfig(BaseSettings):
    """
    Configuration settings for the alerts feature.

    This configuration holds token for authenticating webhook alerts.

    Attributes:
        webhook_alerts_token (str): The token to authenticate for webhook alerts.

    """

    webhook_alerts_token: str = Field(default="", description="The token to authenticate for webhook alerts.")
    alert_colors: Dict[str, discord.Color] = Field(
        default={
            "service_down": discord.Color.red(),
            "service_degraded": discord.Color.yellow(),
            "service_restarting": discord.Color.yellow(),
            "service_restart_failed": discord.Color.red(),
            "service_restart_succeeded": discord.Color.green(),
        },
        description="A dictionary mapping alert types to colors.",
    )


alerts_config = AlertsConfig()
