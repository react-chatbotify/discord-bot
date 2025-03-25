"""
CogsManagerConfig module for loading cogs.

This module defines configuration settings for the bot's cogs manager.
It uses Pydantic for validation and loading of environment- based or
default values related to the loading of modules.
"""

from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode


class CogsManagerConfig(BaseSettings):
    """
    Configuration settings for the cogs manager.

    This configuration holds modules to be loaded.

    Attributes:
        loaded_modules (List[str]): The list of modules to be loaded.

    """

    # todo: add user welcome module
    # todo: add healthchecks module
    # todo: add moderation module (can explore a touch of AI moderation as well with: https://perspectiveapi.com/)
    # todo: add polls module
    loaded_modules: Annotated[List[str], NoDecode] = Field(
        default_factory=list, description="The list of modules to be loaded."
    )

    @field_validator("loaded_modules", mode="before")
    @classmethod
    def split_loaded_modules(cls, v):
        """
        Convert a comma-separated string to a list of module names.

        Args:
            v (str | list): The raw value from the environment or settings.

        Returns:
            list[str]: A list of cleaned module names.

        """
        if isinstance(v, str):
            return [module.strip() for module in v.split(",") if module.strip()]
        return v


cogs_manager_config = CogsManagerConfig()
