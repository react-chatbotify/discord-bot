"""
LoggingConfig module for configuring Discord bot logging behavior.

This module defines settings related to logging, including the target
Discord channel for logs, logging level, formatting, and logger prefix.
It uses Pydantic to manage and validate environment-based or default
values.
"""

from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode


class LoggingConfig(BaseSettings):
    """
    Configuration settings for Discord bot logging.

    This configuration controls logging output, including channel targeting,
    formatting, and log levels.

    Attributes:
        log_channel_id (int): The Discord channel ID where logs should be sent.
        logger_level (str): The logging level (e.g., 'info', 'debug', 'warning').
        logger_prefix (str): The logger name/prefix used in log entries.
        logger_format (str): The format string for log messages.
        logged_actions (List[str]): The list of actions to be logged.

    """

    log_channel_id: int = Field(
        default=0,
        description="The Discord channel ID where logs should be posted.",
    )
    logger_level: str = Field(
        default="info",
        description="The logging level used by the logger (e.g., 'info', 'debug').",
    )
    logger_prefix: str = Field(
        default="discord",
        description="The prefix or logger name used in logs.",
    )
    logger_format: str = Field(
        default="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        description="The format string used for log messages.",
    )
    logged_actions: Annotated[List[str], NoDecode] = Field(
        default_factory=list, description="The list of actions to be logged."
    )

    @field_validator("logged_actions", mode="before")
    @classmethod
    def split_logged_actions(cls, v):
        """
        Convert a comma-separated string to a list of actions to be logged.

        Args:
            v (str | list): The raw value from the environment or settings.

        Returns:
            list[str]: A list of actions to be logged.

        """
        if isinstance(v, str):
            return [action.strip().lower() for action in v.split(",") if action.strip()]
        return v


logging_config = LoggingConfig()
