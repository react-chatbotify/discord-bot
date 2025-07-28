"""
Alerts module for managing webhook alerts.

This module defines configuration settings for receiving webhook alerts.
"""

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


alerts_config = AlertsConfig()
