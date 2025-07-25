"""
Prompt module for representing a prompt object.

This module contains a Pydantic model that represents the structure and
behavior of a prompt. It includes attributes for title, description,
content, and a custom ID used to identify the prompt.
"""

from pydantic import BaseModel, Field


class Prompt(BaseModel):
    """
    Pydantic model representing a prompt configuration.

    This model defines the attributes required to construct and manage
    a prompt, including its title, description, content, and custom ID.

    Attributes:
        custom_id (str): Unique identifier for the prompt.
        title (str): The title of the prompt.
        description (str): A short description of the prompt.
        content (str): The main content or text of the prompt.

    """

    custom_id: str = Field(..., description="Unique identifier for the prompt.")
    title: str = Field(..., description="The title of the prompt.")
    description: str = Field(..., description="A short description of the prompt.")
    content: str = Field(..., description="The main content or text of the prompt.")
